from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models import User

# Create your models here.
class Project(models.Model):  
    title = models.CharField(max_length=100)  
    description = models.TextField()  
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', null=True)  
    image = models.ImageField(upload_to='images', null=True)  

    def _str_(self):
        return self.title

    def total_tasks(self):
        return sum(bug.total_task for bug in self.bug_set.all())

    def complete_tasks(self):
        return sum(bug.complete_task for bug in self.bug_set.all())

  
