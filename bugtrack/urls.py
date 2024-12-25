from django.urls import path
from bugtrack  import views as b
from project import views as p
urlpatterns = [
    path('bugs/<int:project_id>', b.bugList, name='bug_list'),
    path('bug_create/project/<int:project_id>/', b.addBug, name='bug_create'),
    path('update_status/<str:bug_id>/<str:status>/', b.updateStatus, name='update_status'),
    path('delete_bug/<int:bug_id>/', b.deleteBug, name='delete_bug'),
    path('update_due_date/<int:bug_id>/', b.updateDueDate, name='update_due_date'),          
]

