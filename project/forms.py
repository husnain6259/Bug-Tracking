from django import forms
from project.models import Project
# from django.contrib.auth.forms import UserCreationForm

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description','image']
