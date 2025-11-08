"""
Views for events and reminders.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from datetime import timedelta
from .models import Event, Reminder
from .forms import EventForm, ReminderForm, ReminderFilterForm


@login_required
def events_hub(request):
    """Display all events and reminders for the user."""
    user = request.user
    
    # Get all events
    events = Event.objects.filter(user=user).order_by('start_date')
    
    # Get all reminders
    reminders = Reminder.objects.filter(user=user).order_by('reminder_date')
    
    # Get pending reminders (not completed and not sent)
    pending_reminders = reminders.filter(is_completed=False)
    
    # Get upcoming events and reminders (next 30 days)
    now = timezone.now()
    upcoming_events = events.filter(start_date__gte=now, start_date__lt=now + timedelta(days=30))
    upcoming_reminders = reminders.filter(
        reminder_date__gte=now,
        reminder_date__lt=now + timedelta(days=30)
    )
    
    context = {
        'events': events,
        'reminders': reminders,
        'pending_reminders': pending_reminders,
        'upcoming_events': upcoming_events,
        'upcoming_reminders': upcoming_reminders,
    }
    return render(request, 'events/hub.html', context)


@login_required
def event_list(request):
    """Display list of events with filtering."""
    user = request.user
    events = Event.objects.filter(user=user).order_by('start_date')
    
    # Filtering
    event_type = request.GET.get('event_type')
    if event_type:
        events = events.filter(event_type=event_type)
    
    course = request.GET.get('course')
    if course:
        events = events.filter(course_id=course)
    
    # Search
    search = request.GET.get('search')
    if search:
        events = events.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    
    context = {
        'events': events,
        'active_tab': 'events',
    }
    return render(request, 'events/event_list.html', context)


@login_required
def event_create(request):
    """Create a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Create Event',
        'active_tab': 'events',
    }
    return render(request, 'events/event_form.html', context)


@login_required
def event_detail(request, pk):
    """Display event details and reminders."""
    event = get_object_or_404(Event, pk=pk, user=request.user)
    reminder = event.reminder if hasattr(event, 'reminder') else None
    
    context = {
        'event': event,
        'reminder': reminder,
        'active_tab': 'events',
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_update(request, pk):
    """Update an event."""
    event = get_object_or_404(Event, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event, user=request.user)
    
    context = {
        'form': form,
        'event': event,
        'page_title': 'Edit Event',
        'active_tab': 'events',
    }
    return render(request, 'events/event_form.html', context)


@login_required
def event_delete(request, pk):
    """Delete an event."""
    event = get_object_or_404(Event, pk=pk, user=request.user)
    
    if request.method == 'POST':
        event.delete()
        return redirect('event-list')
    
    context = {
        'object': event,
        'active_tab': 'events',
    }
    return render(request, 'events/event_confirm_delete.html', context)


@login_required
def reminder_list(request):
    """Display list of reminders with filtering."""
    user = request.user
    reminders = Reminder.objects.filter(user=user).order_by('reminder_date')
    
    # Filtering
    filter_form = ReminderFilterForm(request.GET)
    
    reminder_type = request.GET.get('reminder_type')
    if reminder_type:
        reminders = reminders.filter(reminder_type=reminder_type)
    
    notification_type = request.GET.get('notification_type')
    if notification_type:
        reminders = reminders.filter(notification_type=notification_type)
    
    is_completed = request.GET.get('is_completed')
    if is_completed == 'true':
        reminders = reminders.filter(is_completed=True)
    elif is_completed == 'false':
        reminders = reminders.filter(is_completed=False)
    
    # Sorting
    sort_by = request.GET.get('sort_by', 'reminder_date')
    reminders = reminders.order_by(sort_by)
    
    # Search
    search = request.GET.get('search')
    if search:
        reminders = reminders.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    context = {
        'reminders': reminders,
        'filter_form': filter_form,
        'active_tab': 'reminders',
    }
    return render(request, 'events/reminder_list.html', context)


@login_required
def reminder_create(request):
    """Create a new reminder."""
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect('reminder_detail', pk=reminder.pk)
    else:
        form = ReminderForm()
    
    context = {
        'form': form,
        'page_title': 'Create Reminder',
        'active_tab': 'reminders',
    }
    return render(request, 'events/reminder_form.html', context)


@login_required
def reminder_detail(request, pk):
    """Display reminder details."""
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    
    context = {
        'reminder': reminder,
        'active_tab': 'reminders',
    }
    return render(request, 'events/reminder_detail.html', context)


@login_required
def reminder_update(request, pk):
    """Update a reminder."""
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('reminder_detail', pk=reminder.pk)
    else:
        form = ReminderForm(instance=reminder)
    
    context = {
        'form': form,
        'reminder': reminder,
        'page_title': 'Edit Reminder',
        'active_tab': 'reminders',
    }
    return render(request, 'events/reminder_form.html', context)


@login_required
def reminder_delete(request, pk):
    """Delete a reminder."""
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    
    if request.method == 'POST':
        reminder.delete()
        return redirect('reminder-list')
    
    context = {
        'object': reminder,
        'active_tab': 'reminders',
    }
    return render(request, 'events/reminder_confirm_delete.html', context)


@login_required
def reminder_mark_complete(request, pk):
    """Mark reminder as complete."""
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    
    if request.method == 'POST':
        reminder.is_completed = True
        reminder.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'is_completed': reminder.is_completed})
        return redirect('reminder-list')
    
    context = {
        'reminder': reminder,
        'active_tab': 'reminders',
    }
    return render(request, 'events/reminder_mark_complete.html', context)


@login_required
def api_upcoming_events(request):
    """API endpoint for upcoming events (next 7 days)."""
    user = request.user
    now = timezone.now()
    upcoming = Event.objects.filter(
        user=user,
        start_date__gte=now,
        start_date__lt=now + timedelta(days=7)
    ).order_by('start_date').values('id', 'title', 'event_type', 'start_date')
    
    return JsonResponse({
        'events': list(upcoming)
    })


@login_required
def api_upcoming_reminders(request):
    """API endpoint for pending reminders."""
    user = request.user
    now = timezone.now()
    pending = Reminder.objects.filter(
        user=user,
        is_completed=False,
        reminder_date__gte=now,
        reminder_date__lt=now + timedelta(days=7)
    ).order_by('reminder_date').values('id', 'title', 'reminder_type', 'reminder_date')
    
    return JsonResponse({
        'reminders': list(pending)
    })
