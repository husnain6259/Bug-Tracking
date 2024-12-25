from django import forms
from bugtrack.models import Bug
# from django.contrib.auth.forms import UserCreationForm

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description', 'type', 'status', 'due_date', 'assigned_to','image']



