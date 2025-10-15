"""
Views for the assignments app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
