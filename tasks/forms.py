from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'task_name', 'description', 'assigned_to', 'due_date', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }