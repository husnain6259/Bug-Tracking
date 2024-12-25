from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models import User
from project.models import Project

class Bug(models.Model):  
    STATUS_CHOICES = (  
        ('Pending', 'Pending'),  
        ('In Progress', 'In Progress'),  
        ('Completed', 'Completed'),  
        ('Closed', 'Closed'),  
    )  
    TYPE_CHOICES = (  
        ('Bug', 'Bug'),  
        ('Feature', 'Feature'),  
    )  
    title = models.CharField(max_length=100)  
    description = models.TextField()  
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)  
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')  
    due_date = models.DateField()  
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)  
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projects',null=True)  
    image = models.ImageField(upload_to='images', null=True)  
    total_tasks = models.IntegerField(default=0)  
    completed_tasks = models.IntegerField(default=0)  

    def __str__(self):  
        return self.title
