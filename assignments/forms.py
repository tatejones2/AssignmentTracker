"""
Forms for the assignments app.
"""
from django import forms
from datetime import datetime, time, timedelta
from .models import Assignment, Course


class CourseForm(forms.ModelForm):
    """Form for creating and updating courses."""
    
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'professor', 'credits', 'semester', 'color', 'description']
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'professor': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'semester': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class AssignmentForm(forms.ModelForm):
    """Form for creating and updating assignments."""
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(user=user)
        
        # Set default time to 11:59 PM on the closest upcoming Sunday if no instance provided
        if not self.instance.pk and not self.initial.get('due_date'):
            now = datetime.now()
            # Calculate days until next Sunday (6 = Sunday)
            days_until_sunday = (6 - now.weekday()) % 7
            # If today is Sunday (weekday() == 6), set to next Sunday
            if days_until_sunday == 0:
                days_until_sunday = 7
            next_sunday = now + timedelta(days=days_until_sunday)
            default_datetime = datetime.combine(next_sunday.date(), time(23, 59))
            self.fields['due_date'].initial = default_datetime
    
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
            'course': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
