"""
Admin configuration for assignments app.
"""
from django.contrib import admin
from .models import Assignment, Course, Podcast, StudyNotes, Event, Reminder


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""
    
    list_display = ['course_code', 'course_name', 'professor', 'credits', 'semester', 'user', 'assignment_count']
    list_filter = ['semester', 'credits', 'user']
    search_fields = ['course_code', 'course_name', 'professor']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course_code', 'course_name', 'professor', 'credits', 'semester')
        }),
        ('Customization', {
            'fields': ('color', 'description')
        }),
        ('User', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Admin interface for Assignment model."""
    
    list_display = ['title', 'course', 'due_date', 'status', 'priority', 'user', 'created_at']
    list_filter = ['status', 'priority', 'course', 'due_date', 'user']
    search_fields = ['title', 'course', 'description']
    date_hierarchy = 'due_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'course')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('User', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    """Admin interface for Podcast model."""
    
    list_display = ['title', 'topic', 'tone', 'length', 'is_generated', 'is_audio_generated', 'user', 'created_at']
    list_filter = ['tone', 'length', 'is_generated', 'is_audio_generated', 'user']
    search_fields = ['title', 'topic']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StudyNotes)
class StudyNotesAdmin(admin.ModelAdmin):
    """Admin interface for StudyNotes model."""
    
    list_display = ['topic', 'detail_level', 'is_generated', 'user', 'created_at']
    list_filter = ['detail_level', 'is_generated', 'user']
    search_fields = ['topic']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model."""
    
    list_display = ['title', 'event_type', 'start_date', 'course', 'user', 'created_at']
    list_filter = ['event_type', 'start_date', 'course', 'user']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'event_type', 'location')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date')
        }),
        ('Related Info', {
            'fields': ('course', 'user')
        }),
        ('Display', {
            'fields': ('color',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """Admin interface for Reminder model."""
    
    list_display = ['title', 'reminder_type', 'reminder_date', 'notification_type', 'is_completed', 'is_sent', 'user']
    list_filter = ['reminder_type', 'notification_type', 'is_completed', 'is_sent', 'reminder_date', 'user']
    search_fields = ['title', 'description']
    date_hierarchy = 'reminder_date'
    readonly_fields = ['created_at', 'updated_at', 'is_sent']
    
    fieldsets = (
        ('Reminder Information', {
            'fields': ('title', 'description', 'reminder_type')
        }),
        ('Date & Time', {
            'fields': ('reminder_date',)
        }),
        ('Related Items', {
            'fields': ('event', 'assignment')
        }),
        ('Notifications', {
            'fields': ('notification_type', 'is_sent')
        }),
        ('Status', {
            'fields': ('is_completed',)
        }),
        ('User', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
