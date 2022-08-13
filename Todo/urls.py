from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView

from .views import *

app_name = 'Todo'

urlpatterns = [
    path('', Todo_todo, name='todo'),
    path('login/', Todo_login, name='login'),
    path('register/', Todo_register, name='register'),
    path('logout/', Todo_logout, name='logout'),

    path('ajax/add-task/', Todo_add_task, name='add_task'),

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]
