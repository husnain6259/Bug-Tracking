# ab jo views hum ny banya ha us k redirect krny k liye url b chaye
from django.urls import path
from . import views

urlpatterns=[
    path('projects/',views.getRoute),
    path('projects',views.getProjects),
    path('projects/<str:pk>/',views.getProjects),
    path('add/',views.addProject),
    path('update/',views.updateProject),

]