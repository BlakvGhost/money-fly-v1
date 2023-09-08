from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('forgot-password', views.new_password, name="password.forgot"),
    path('logout', views.logout, name="logout"),
]