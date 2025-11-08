"""
Forms for the assignments app.
"""
from django import forms
from django.utils import timezone
from datetime import datetime, time, timedelta
from .models import Assignment, Course, Podcast, StudyNotes, Event, Reminder


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
            now = timezone.now()
            # Calculate days until next Sunday (6 = Sunday)
            days_until_sunday = (6 - now.weekday()) % 7
            # If today is Sunday (weekday() == 6), set to next Sunday
            if days_until_sunday == 0:
                days_until_sunday = 7
            next_sunday = now + timedelta(days=days_until_sunday)
            # Set time to 11:59 PM in the configured timezone
            default_datetime = timezone.make_aware(datetime.combine(next_sunday.date(), time(23, 59)))
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
        fields = ['title', 'topic', 'notes_text', 'notes_file', 'tone', 'length', 'course', 'description']
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
            'notes_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.txt,.pdf,.docx,.doc',
                'help_text': 'Upload a document (TXT, PDF, DOCX)'
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


class StudyNotesForm(forms.ModelForm):
    """Form for generating AI study notes."""
    
    class Meta:
        model = StudyNotes
        fields = ['topic', 'detail_level', 'course']
        widgets = {
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Photosynthesis, Linear Algebra, World War II...',
                'autofocus': True
            }),
            'detail_level': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(user=user)
        self.fields['course'].required = False


class EventForm(forms.ModelForm):
    """Form for creating and updating events."""
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'start_date', 'end_date', 'location', 'course', 'color']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Midterm Exam, Project Deadline',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any additional details...'
            }),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Room 101, Online, Library'
            }),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(user=user)
        self.fields['course'].required = False
        self.fields['end_date'].required = False
        self.fields['location'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data


class ReminderForm(forms.ModelForm):
    """Form for creating and updating reminders."""
    
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'reminder_type', 'reminder_date', 'notification_type', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Study for Biology, Submit Project',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any notes or details...'
            }),
            'reminder_type': forms.Select(attrs={'class': 'form-control'}),
            'reminder_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'notification_type': forms.Select(attrs={'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ReminderFilterForm(forms.Form):
    """Form for filtering reminders."""
    
    SORT_CHOICES = [
        ('reminder_date', 'Date (Earliest First)'),
        ('-reminder_date', 'Date (Latest First)'),
        ('created_at', 'Recently Created'),
    ]
    
    reminder_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Reminder.REMINDER_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    notification_type = forms.ChoiceField(
        choices=[('', 'All Notifications')] + list(Reminder.NOTIFICATION_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    is_completed = forms.ChoiceField(
        choices=[('', 'All Status'), ('true', 'Completed'), ('false', 'Pending')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='reminder_date',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
