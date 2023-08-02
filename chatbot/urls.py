""" This file is a configuration file for defining URL patterns and 
associating them with corresponding view functions in the Django 
application
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatbot, name='chatbot'),
    path("login", views.login, name='login'),
    path("register", views.register, name='register'),
    path("logout", views.logout, name='logout'),
]