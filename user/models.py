from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser): 
    ROLE_CHOICES = (
        ('is_manager', 'Is Manager'),
        ('is_qa', 'Is qa'),
        ('is_developer', 'Is Developer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,null=True)
    image=models.ImageField(upload_to='images',null=True)