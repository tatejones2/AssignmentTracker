"""
Test cases for Assignment and Course views.
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from assignments.models import Course, Assignment
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestAssignmentViews:
    """Test cases for assignment views."""

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
            course_name='Intro to CS',
            user=user
        )

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return Client()

    @pytest.fixture
    def authenticated_client(self, client, user):
        """Create an authenticated test client."""
        client.login(username='testuser', password='testpass123')
        return client

    def test_assignment_list_requires_login(self, client):
        """Test that assignment list requires login."""
        response = client.get(reverse('assignment_list'))
        assert response.status_code == 302  # Redirect to login

    def test_assignment_list_view(self, authenticated_client, user, course):
        """Test the assignment list view."""
        Assignment.objects.create(
            title='Test Assignment',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        
        response = authenticated_client.get(reverse('assignment_list'))
        assert response.status_code == 200
        assert 'Test Assignment' in response.content.decode()

    def test_assignment_create_view_get(self, authenticated_client):
        """Test GET request to assignment create view."""
        response = authenticated_client.get(reverse('assignment_create'))
        assert response.status_code == 200
        assert 'Create' in response.content.decode()

    def test_assignment_create_view_post(self, authenticated_client, user, course):
        """Test POST request to create an assignment."""
        data = {
            'title': 'New Assignment',
            'description': 'Test description',
            'course': course.id,
            'due_date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M'),
            'status': 'not_started',
            'priority': 'high'
        }
        response = authenticated_client.post(reverse('assignment_create'), data)
        assert response.status_code == 302  # Redirect after success
        assert Assignment.objects.filter(title='New Assignment').exists()

    def test_assignment_update_view(self, authenticated_client, user, course):
        """Test updating an assignment."""
        assignment = Assignment.objects.create(
            title='Original Title',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        
        data = {
            'title': 'Updated Title',
            'course': course.id,
            'due_date': assignment.due_date.strftime('%Y-%m-%dT%H:%M'),
            'status': 'in_progress',
            'priority': 'high'
        }
        response = authenticated_client.post(
            reverse('assignment_update', kwargs={'pk': assignment.pk}),
            data
        )
        assert response.status_code == 302
        assignment.refresh_from_db()
        assert assignment.title == 'Updated Title'
        assert assignment.status == 'in_progress'

    def test_assignment_delete_view(self, authenticated_client, user, course):
        """Test deleting an assignment."""
        assignment = Assignment.objects.create(
            title='To Delete',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        
        response = authenticated_client.post(
            reverse('assignment_delete', kwargs={'pk': assignment.pk})
        )
        assert response.status_code == 302
        assert not Assignment.objects.filter(pk=assignment.pk).exists()

    def test_assignment_detail_view(self, authenticated_client, user, course):
        """Test the assignment detail view."""
        assignment = Assignment.objects.create(
            title='Detail Test',
            description='Test description',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        
        response = authenticated_client.get(
            reverse('assignment_detail', kwargs={'pk': assignment.pk})
        )
        assert response.status_code == 200
        assert 'Detail Test' in response.content.decode()
        assert 'Test description' in response.content.decode()


@pytest.mark.django_db
class TestCourseViews:
    """Test cases for course views."""

    @pytest.fixture
    def user(self):
        """Create a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return Client()

    @pytest.fixture
    def authenticated_client(self, client, user):
        """Create an authenticated test client."""
        client.login(username='testuser', password='testpass123')
        return client

    def test_course_list_requires_login(self, client):
        """Test that course list requires login."""
        response = client.get(reverse('course_list'))
        assert response.status_code == 302  # Redirect to login

    def test_course_list_view(self, authenticated_client, user):
        """Test the course list view."""
        Course.objects.create(
            course_code='CS101',
            course_name='Intro to CS',
            user=user
        )
        
        response = authenticated_client.get(reverse('course_list'))
        assert response.status_code == 200
        assert 'CS101' in response.content.decode()

    def test_course_create_view_get(self, authenticated_client):
        """Test GET request to course create view."""
        response = authenticated_client.get(reverse('course_create'))
        assert response.status_code == 200
        assert 'Create' in response.content.decode()

    def test_course_create_view_post(self, authenticated_client):
        """Test POST request to create a course."""
        data = {
            'course_code': 'MATH101',
            'course_name': 'Calculus I',
            'professor': 'Dr. Johnson',
            'credits': 3.0,
            'semester': 'Fall 2025',
            'color': '#00274c'
        }
        response = authenticated_client.post(reverse('course_create'), data)
        assert response.status_code == 302  # Redirect after success
        assert Course.objects.filter(course_code='MATH101').exists()

    def test_course_update_view(self, authenticated_client, user):
        """Test updating a course."""
        course = Course.objects.create(
            course_code='CS101',
            course_name='Original Name',
            user=user
        )
        
        data = {
            'course_code': 'CS101',
            'course_name': 'Updated Name',
            'credits': 3.0,
            'color': '#CC0000'
        }
        response = authenticated_client.post(
            reverse('course_update', kwargs={'pk': course.pk}),
            data
        )
        assert response.status_code == 302
        course.refresh_from_db()
        assert course.course_name == 'Updated Name'

    def test_course_delete_view(self, authenticated_client, user):
        """Test deleting a course."""
        course = Course.objects.create(
            course_code='CS101',
            course_name='To Delete',
            user=user
        )
        
        response = authenticated_client.post(
            reverse('course_delete', kwargs={'pk': course.pk})
        )
        assert response.status_code == 302
        assert not Course.objects.filter(pk=course.pk).exists()

    def test_course_detail_view(self, authenticated_client, user):
        """Test the course detail view."""
        course = Course.objects.create(
            course_code='CS101',
            course_name='Intro to CS',
            professor='Dr. Smith',
            user=user
        )
        
        response = authenticated_client.get(
            reverse('course_detail', kwargs={'pk': course.pk})
        )
        assert response.status_code == 200
        assert 'CS101' in response.content.decode()
        assert 'Dr. Smith' in response.content.decode()

    def test_course_detail_shows_assignments(self, authenticated_client, user):
        """Test that course detail view shows related assignments."""
        course = Course.objects.create(
            course_code='CS101',
            course_name='Intro to CS',
            user=user
        )
        Assignment.objects.create(
            title='Homework 1',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        
        response = authenticated_client.get(
            reverse('course_detail', kwargs={'pk': course.pk})
        )
        assert response.status_code == 200
        assert 'Homework 1' in response.content.decode()
