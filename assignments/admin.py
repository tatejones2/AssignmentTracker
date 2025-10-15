"""
Admin configuration for assignments app.
"""
from django.contrib import admin
from .models import Assignment, Course


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
