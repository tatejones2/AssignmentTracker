from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Course(models.Model):
    """Model representing a course/class."""
    
    COLOR_CHOICES = [
        ('#00274c', 'Navy'),
        ('#CC0000', 'Red'),
        ('#0077b6', 'Blue'),
        ('#2a9d8f', 'Teal'),
        ('#e76f51', 'Orange'),
        ('#9b59b6', 'Purple'),
        ('#16a085', 'Green'),
        ('#e74c3c', 'Crimson'),
    ]
    
    course_code = models.CharField(max_length=20, help_text="e.g., CS101, MATH201")
    course_name = models.CharField(max_length=200, help_text="e.g., Introduction to Programming")
    professor = models.CharField(max_length=100, blank=True)
    credits = models.DecimalField(max_digits=3, decimal_places=1, default=3.0)
    semester = models.CharField(max_length=50, blank=True, help_text="e.g., Fall 2025")
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#00274c')
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course_code']
        unique_together = ['course_code', 'user']
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
    def assignment_count(self):
        """Return the number of assignments for this course."""
        return self.assignments.count()
    
    def pending_assignments(self):
        """Return the number of pending assignments."""
        return self.assignments.exclude(status='completed').count()


class Assignment(models.Model):
    """Model representing a student assignment."""
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.title} - {self.course.course_code}"
    
    def is_overdue(self):
        """Check if assignment is past due date and not completed."""
        return timezone.now() > self.due_date and self.status != 'completed'


class Podcast(models.Model):
    """Model for AI-generated podcasts from notes."""
    
    TONE_CHOICES = [
        ('casual', 'Casual & Fun'),
        ('professional', 'Professional'),
        ('educational', 'Educational'),
        ('motivational', 'Motivational'),
    ]
    
    LENGTH_CHOICES = [
        ('short', 'Short (5-10 min)'),
        ('medium', 'Medium (10-20 min)'),
        ('long', 'Long (20+ min)'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=300, help_text="Topic or subject of the podcast")
    notes_text = models.TextField(help_text="Notes or content to turn into a podcast")
    script = models.TextField(blank=True, help_text="AI-generated podcast script")
    audio_file = models.FileField(upload_to='podcasts/audio/', blank=True, null=True)
    
    tone = models.CharField(max_length=20, choices=TONE_CHOICES, default='educational')
    length = models.CharField(max_length=20, choices=LENGTH_CHOICES, default='medium')
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='podcasts', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='podcasts')
    
    is_generated = models.BooleanField(default=False, help_text="Whether the podcast has been generated")
    is_audio_generated = models.BooleanField(default=False, help_text="Whether audio has been generated")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
