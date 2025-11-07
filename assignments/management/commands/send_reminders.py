"""
Management command to send email reminders for upcoming assignments.
Checks for assignments due in the next 24 hours and 1 week.
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from assignments.models import Assignment


class Command(BaseCommand):
    help = 'Send email reminders for upcoming assignments'

    def handle(self, *args, **options):
        today = timezone.now()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)

        # Check for assignments due in 24 hours
        due_tomorrow = Assignment.objects.filter(
            due_date__gte=today,
            due_date__lte=tomorrow,
            status__in=['not_started', 'in_progress']
        ).select_related('user', 'course')

        # Check for assignments due in 7 days
        due_next_week = Assignment.objects.filter(
            due_date__gte=today,
            due_date__lte=next_week,
            status__in=['not_started', 'in_progress']
        ).exclude(
            id__in=due_tomorrow.values_list('id', flat=True)
        ).select_related('user', 'course')

        # Group by user for due tomorrow
        users_due_tomorrow = {}
        for assignment in due_tomorrow:
            if assignment.user not in users_due_tomorrow:
                users_due_tomorrow[assignment.user] = []
            users_due_tomorrow[assignment.user].append(assignment)

        # Send reminders for due tomorrow
        for user, assignments in users_due_tomorrow.items():
            subject = f'⏰ Reminder: {len(assignments)} assignment(s) due tomorrow!'
            context = {
                'user': user,
                'assignments': assignments,
                'reminder_type': '24 hours',
            }
            html_message = render_to_string('emails/reminder_email.html', context)
            send_mail(
                subject,
                f'You have {len(assignments)} assignment(s) due tomorrow!',
                'noreply@trax.local',
                [user.email],
                html_message=html_message,
                fail_silently=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Sent 24-hour reminder to {user.email}'
                )
            )

        # Group by user for due next week
        users_due_next_week = {}
        for assignment in due_next_week:
            if assignment.user not in users_due_next_week:
                users_due_next_week[assignment.user] = []
            users_due_next_week[assignment.user].append(assignment)

        # Send reminders for due next week
        for user, assignments in users_due_next_week.items():
            subject = f'📅 Reminder: {len(assignments)} assignment(s) coming up this week'
            context = {
                'user': user,
                'assignments': assignments,
                'reminder_type': '7 days',
            }
            html_message = render_to_string('emails/reminder_email.html', context)
            send_mail(
                subject,
                f'You have {len(assignments)} assignment(s) coming up this week!',
                'noreply@trax.local',
                [user.email],
                html_message=html_message,
                fail_silently=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Sent 7-day reminder to {user.email}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS('Email reminders sent successfully!')
        )
