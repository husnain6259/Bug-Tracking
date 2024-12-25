from django.urls import path
from user import views

urlpatterns = [
    path('join', views.joinUs, name='join'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutView, name='logout'),
]