from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'title', 'description', 'start_date', 'deadline', 'status', 'assigned_team']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'assigned_team': forms.CheckboxSelectMultiple,
        }