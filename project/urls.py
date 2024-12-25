from django.urls import path
from project import views as p
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', p.index, name='index'),
    path('project-create/', p.addProject, name='project-create'),
]