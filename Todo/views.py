from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

import requests

from .models import *
from .auth_methods import convert_to_hash


# Create your views here.

def Todo_todo(request):
    context = {}

    if not request.session["login"]:
        return redirect(reverse('Todo:login'))

    return render(request, 'Todo.html', context)


def Todo_login(request):
    context = {
        'site-setting': settings.RECAPTCHA_SITE_KEY,
    }

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        secret_key = settings.RECAPTCHA_SECRET_KEY

        # todo check this
        # captcha verification
        data = {
            'response': request.POST.get('g-recaptcha-response'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()

        print(result_json)

        if not result_json.get('success'):
            pass
            # return render(request, 'contact_sent.html', {'is_robot': True})
        # end captcha verification

        password = convert_to_hash(password)

        try:
            member = Members.objects.get(username=username)
            if password == member.password:
                request.session["login"] = True
                request.session["id"] = member.id
                request.session.set_expiry(24 * 60 * 60)
                return redirect(reverse('Todo:todo'))
            else:
                request.session["login"] = False
                request.session["id"] = None
                messages.add_message(request, messages.ERROR, 'Password is incorrect')

        except Members.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'User does not exist')

    return render(request, 'login.html', context)


def Todo_add_task(request):
    if not request.session["login"]:
        return redirect(reverse('Todo:login'))

    if request.POST:
        user_id = request.session["id"]
        text = request.Post.get('text')
        priority = request.Post.get('priority')

        Task.objects.create(user_id=user_id, text=text, priority=priority)
        messages.add_message(request, messages.SUCCESS, 'Task added successfully')


def Todo_check_Task(request):
    if not request.session["login"]:
        return redirect(reverse('Todo:login'))

    if request.POST:
        status = request.POST.get('status')
        task_id = request.POST.get('task_id')

        try:
            task = Task.objects.get(id=task_id)
            task.done = bool(status)
            task.save()
            messages.add_message(request, messages.SUCCESS, 'Task updated successfully')

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Task Not FOund')


def Todo_edit_task(request):
    if not request.session["login"]:
        return redirect(reverse('Todo:login'))

    if request.POST:
        task_id = request.POST.get('task_id')
        text = request.POST.get('text')
        priority = request.POST.get('priority')

        try:
            task = Task.objects.get(id=task_id)
            task.text = text
            task.priority = priority
            task.save()
            messages.add_message(request, messages.SUCCESS, 'Task edited successfully')

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Task Not FOund')
