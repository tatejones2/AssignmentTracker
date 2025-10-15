"""
Test cases for Assignment model.
"""
import pytest
from django.contrib.auth.models import User
from assignments.models import Course, Assignment
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestAssignmentModel:
    """Test cases for the Assignment model."""

    @pytest.fixture
    def user(self):
        """Create a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    @pytest.fixture
    def course(self, user):
        """Create a test course."""
        return Course.objects.create(
            course_code='CS101',
            course_name='Introduction to Computer Science',
            user=user
        )

    @pytest.fixture
    def assignment(self, course, user):
        """Create a test assignment."""
        return Assignment.objects.create(
            title='Homework 1',
            description='Complete exercises 1-10',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            status='not_started',
            priority='medium',
            user=user
        )

    def test_assignment_creation(self, assignment):
        """Test that an assignment can be created."""
        assert assignment.title == 'Homework 1'
        assert assignment.description == 'Complete exercises 1-10'
        assert assignment.status == 'not_started'
        assert assignment.priority == 'medium'
        assert assignment.user is not None
        assert assignment.course is not None

    def test_assignment_str_method(self, assignment):
        """Test the string representation of an assignment."""
        expected = "Homework 1 - CS101"
        assert str(assignment) == expected

    def test_assignment_is_overdue_false(self, course, user):
        """Test is_overdue returns False for future assignments."""
        future_assignment = Assignment.objects.create(
            title='Future Assignment',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            status='not_started',
            user=user
        )
        assert future_assignment.is_overdue() is False

    def test_assignment_is_overdue_true(self, course, user):
        """Test is_overdue returns True for past due assignments."""
        overdue_assignment = Assignment.objects.create(
            title='Overdue Assignment',
            course=course,
            due_date=timezone.now() - timedelta(days=1),
            status='not_started',
            user=user
        )
        assert overdue_assignment.is_overdue() is True

    def test_assignment_is_overdue_completed(self, course, user):
        """Test is_overdue returns False for completed assignments."""
        completed_assignment = Assignment.objects.create(
            title='Completed Assignment',
            course=course,
            due_date=timezone.now() - timedelta(days=1),
            status='completed',
            user=user
        )
        assert completed_assignment.is_overdue() is False

    def test_assignment_status_choices(self, course, user):
        """Test that different status values work."""
        statuses = ['not_started', 'in_progress', 'completed']
        for status in statuses:
            assignment = Assignment.objects.create(
                title=f'Test {status}',
                course=course,
                due_date=timezone.now() + timedelta(days=7),
                status=status,
                user=user
            )
            assert assignment.status == status

    def test_assignment_priority_choices(self, course, user):
        """Test that different priority values work."""
        priorities = ['low', 'medium', 'high']
        for priority in priorities:
            assignment = Assignment.objects.create(
                title=f'Test {priority}',
                course=course,
                due_date=timezone.now() + timedelta(days=7),
                priority=priority,
                user=user
            )
            assert assignment.priority == priority

    def test_assignment_ordering(self, course, user):
        """Test that assignments are ordered by due_date."""
        Assignment.objects.create(
            title='Third',
            course=course,
            due_date=timezone.now() + timedelta(days=15),
            user=user
        )
        Assignment.objects.create(
            title='First',
            course=course,
            due_date=timezone.now() + timedelta(days=5),
            user=user
        )
        Assignment.objects.create(
            title='Second',
            course=course,
            due_date=timezone.now() + timedelta(days=10),
            user=user
        )
        
        assignments = list(Assignment.objects.filter(user=user))
        assert assignments[0].title == 'First'
        assert assignments[1].title == 'Second'
        assert assignments[2].title == 'Third'

    def test_assignment_timestamps(self, assignment):
        """Test that created_at and updated_at are set."""
        assert assignment.created_at is not None
        assert assignment.updated_at is not None
        assert assignment.created_at <= assignment.updated_at

    def test_assignment_optional_description(self, course, user):
        """Test that description is optional."""
        assignment = Assignment.objects.create(
            title='No Description',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        assert assignment.description == ''

    def test_assignment_default_values(self, course, user):
        """Test that default values are set correctly."""
        assignment = Assignment.objects.create(
            title='Default Values',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        assert assignment.status == 'not_started'
        assert assignment.priority == 'medium'
