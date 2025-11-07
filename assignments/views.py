"""
Views for the assignments app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
import calendar as cal
from .models import Assignment, Course
from .forms import AssignmentForm, CourseForm


@login_required
def assignment_list(request):
    """Display list of all assignments for the logged-in user."""
    assignments = Assignment.objects.filter(user=request.user)
    context = {
        'assignments': assignments,
    }
    return render(request, 'assignments/assignment_list.html', context)


@login_required
def dashboard(request):
    """Display dashboard with overview of assignments and courses."""
    user = request.user
    today = timezone.now().date()
    
    # Get all assignments and courses for user
    all_assignments = Assignment.objects.filter(user=user)
    all_courses = Course.objects.filter(user=user)
    
    # Get upcoming assignments (next 7 days)
    upcoming_date = today + timedelta(days=7)
    upcoming_assignments = all_assignments.filter(
        due_date__date__gte=today,
        due_date__date__lte=upcoming_date
    ).order_by('due_date')[:5]
    
    # Get overdue assignments
    overdue_assignments = all_assignments.exclude(
        status='completed'
    ).filter(
        due_date__date__lt=today
    ).order_by('due_date')
    
    # Get completed assignments this week
    week_start = today - timedelta(days=today.weekday())
    completed_this_week = all_assignments.filter(
        status='completed',
        updated_at__date__gte=week_start
    ).count()
    
    # Calculate statistics
    total_assignments = all_assignments.count()
    completed_assignments = all_assignments.filter(status='completed').count()
    in_progress = all_assignments.filter(status='in_progress').count()
    not_started = all_assignments.filter(status='not_started').count()
    completion_percentage = round((completed_assignments / total_assignments * 100) if total_assignments > 0 else 0)
    
    # Get assignments due today
    due_today = all_assignments.filter(due_date__date=today)
    
    context = {
        'today': today,
        'upcoming_assignments': upcoming_assignments,
        'overdue_assignments': overdue_assignments,
        'due_today': due_today,
        'all_courses': all_courses,
        'total_assignments': total_assignments,
        'completed_assignments': completed_assignments,
        'in_progress': in_progress,
        'not_started': not_started,
        'completion_percentage': completion_percentage,
        'completed_this_week': completed_this_week,
    }
    return render(request, 'assignments/dashboard.html', context)


@login_required
def assignment_create(request):
    """Create a new assignment."""
    if request.method == 'POST':
        form = AssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(user=request.user)
    context = {
        'form': form,
        'action': 'Create'
    }
    return render(request, 'assignments/assignment_form.html', context)


@login_required
def assignment_update(request, pk):
    """Update an existing assignment."""
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment, user=request.user)
    context = {
        'form': form,
        'action': 'Update',
        'assignment': assignment
    }
    return render(request, 'assignments/assignment_form.html', context)


@login_required
def assignment_delete(request, pk):
    """Delete an assignment."""
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully!')
        return redirect('assignment_list')
    context = {
        'assignment': assignment
    }
    return render(request, 'assignments/assignment_confirm_delete.html', context)


@login_required
def assignment_detail(request, pk):
    """Display detailed view of a single assignment."""
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    context = {
        'assignment': assignment
    }
    return render(request, 'assignments/assignment_detail.html', context)


@login_required
def assignment_complete(request, pk):
    """Mark an assignment as completed."""
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    assignment.status = 'completed'
    assignment.save()
    messages.success(request, f'"{assignment.title}" marked as completed!')
    return redirect('assignment_detail', pk=pk)


@login_required
def calendar_view(request):
    """Display calendar view of assignments."""
    today = timezone.now().date()
    
    # Get month from query parameter or use current month
    month_param = request.GET.get('month')
    if month_param:
        try:
            current_month = datetime.strptime(month_param, '%Y-%m').date().replace(day=1)
        except ValueError:
            current_month = today.replace(day=1)
    else:
        current_month = today.replace(day=1)
    
    # Get the calendar for current month
    cal_obj = cal.monthcalendar(current_month.year, current_month.month)
    
    # Get all assignments for this user
    assignments = Assignment.objects.filter(user=request.user)
    
    # Create a dictionary of dates to assignments
    assignments_by_date = {}
    for assignment in assignments:
        due_date = assignment.due_date.date()
        if due_date not in assignments_by_date:
            assignments_by_date[due_date] = []
        assignments_by_date[due_date].append(assignment)
    
    # Format calendar with assignment data
    calendar_data = []
    for week in cal_obj:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': None, 'assignments': []})
            else:
                date = current_month.replace(day=day)
                assignments_on_day = assignments_by_date.get(date, [])
                week_data.append({
                    'day': day,
                    'date': date,
                    'assignments': assignments_on_day,
                    'is_today': date == today,
                    'is_past': date < today,
                })
        calendar_data.append(week_data)
    
    # Calculate previous and next month
    if current_month.month == 1:
        prev_month = current_month.replace(year=current_month.year - 1, month=12)
    else:
        prev_month = current_month.replace(month=current_month.month - 1)
    
    if current_month.month == 12:
        next_month = current_month.replace(year=current_month.year + 1, month=1)
    else:
        next_month = current_month.replace(month=current_month.month + 1)
    
    context = {
        'current_month': current_month,
        'calendar_data': calendar_data,
        'today': today,
        'month_name': current_month.strftime('%B %Y'),
        'prev_month': prev_month,
        'next_month': next_month,
    }
    return render(request, 'assignments/calendar.html', context)


# Course Views
@login_required
def course_list(request):
    """Display list of all courses for the logged-in user."""
    courses = Course.objects.filter(user=request.user)
    context = {
        'courses': courses,
    }
    return render(request, 'assignments/course_list.html', context)


@login_required
def course_create(request):
    """Create a new course."""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_list')
    else:
        form = CourseForm()
    context = {
        'form': form,
        'action': 'Create'
    }
    return render(request, 'assignments/course_form.html', context)


@login_required
def course_update(request, pk):
    """Update an existing course."""
    course = get_object_or_404(Course, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    context = {
        'form': form,
        'action': 'Update',
        'course': course
    }
    return render(request, 'assignments/course_form.html', context)


@login_required
def course_delete(request, pk):
    """Delete a course."""
    course = get_object_or_404(Course, pk=pk, user=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course_list')
    context = {
        'course': course
    }
    return render(request, 'assignments/course_confirm_delete.html', context)


@login_required
def course_detail(request, pk):
    """Display detailed view of a single course."""
    course = get_object_or_404(Course, pk=pk, user=request.user)
    assignments = course.assignments.all()
    context = {
        'course': course,
        'assignments': assignments,
    }
    return render(request, 'assignments/course_detail.html', context)
