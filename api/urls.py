
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    
    path("user", views.UserAPI.as_view()),
    path("login", views.LoginAPI.as_view()),
    path("event", views.EventAPI.as_view()),
    
]