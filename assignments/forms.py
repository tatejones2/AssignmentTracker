"""
Forms for the assignments app.
"""
from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    """Form for creating and updating assignments."""
    
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'course', 'due_date', 'status', 'priority']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
