
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    
    path("user", views.UserAPI.as_view()),
    path("login", views.LoginAPI.as_view()),
    path("complain", views.ComplainAPI.as_view()),
    path("deletecomplain", views.deleteComplainAPI.as_view()),
    
]