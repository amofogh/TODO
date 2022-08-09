from django.urls import path
from .views import *

app_name = 'Todo'

urlpatterns = [
    path('', Todo_todo, name='todo'),
    path('login', Todo_login, name='login'),

    path('ajax/add-task/', Todo_add_task, name='add_task')
]
