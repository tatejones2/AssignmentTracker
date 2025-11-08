"""
Forms for the assignments app.
"""
from django import forms
from datetime import datetime, time, timedelta
from .models import Assignment, Course, Podcast


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


class AssignmentFilterForm(forms.Form):
    """Form for filtering assignments."""
    
    SORT_CHOICES = [
        ('due_date', 'Due Date (Earliest First)'),
        ('-due_date', 'Due Date (Latest First)'),
        ('priority', 'Priority (High to Low)'),
        ('created_at', 'Recently Created'),
    ]
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        required=False,
        empty_label='All Courses',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(Assignment.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + list(Assignment.PRIORITY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='due_date',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(user=user)


class PodcastForm(forms.ModelForm):
    """Form for creating podcasts from notes."""
    
    class Meta:
        model = Podcast
        fields = ['title', 'topic', 'notes_text', 'tone', 'length', 'course', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Python Basics Study Guide'
            }),
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Introduction to Python, Chapter 1-3'
            }),
            'notes_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Paste your notes, study guide, or any text you want turned into a podcast...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional: Add any additional context or instructions'
            }),
            'tone': forms.Select(attrs={'class': 'form-control'}),
            'length': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(user=user)
        self.fields['course'].required = False
