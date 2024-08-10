from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/login_check/', views.login_check, name='login_check'),
    path('login_check/', views.login_check, name='login_check'),
    path('register_check/', views.register_process, name='register_check'),
]