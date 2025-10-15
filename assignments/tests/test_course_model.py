"""
Test cases for Course model.
"""
import pytest
from django.contrib.auth.models import User
from assignments.models import Course, Assignment
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestCourseModel:
    """Test cases for the Course model."""

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
            professor='Dr. Smith',
            credits=3.0,
            semester='Fall 2025',
            color='#00274c',
            description='Basic programming concepts',
            user=user
        )

    def test_course_creation(self, course):
        """Test that a course can be created."""
        assert course.course_code == 'CS101'
        assert course.course_name == 'Introduction to Computer Science'
        assert course.professor == 'Dr. Smith'
        assert course.credits == 3.0
        assert course.semester == 'Fall 2025'
        assert course.color == '#00274c'
        assert course.user is not None

    def test_course_str_method(self, course):
        """Test the string representation of a course."""
        expected = "CS101 - Introduction to Computer Science"
        assert str(course) == expected

    def test_course_assignment_count(self, course, user):
        """Test that assignment_count returns correct number."""
        # Initially should be 0
        assert course.assignment_count() == 0
        
        # Create an assignment
        Assignment.objects.create(
            title='Homework 1',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        assert course.assignment_count() == 1
        
        # Create another assignment
        Assignment.objects.create(
            title='Homework 2',
            course=course,
            due_date=timezone.now() + timedelta(days=14),
            user=user
        )
        assert course.assignment_count() == 2

    def test_course_pending_assignments(self, course, user):
        """Test that pending_assignments returns correct count."""
        # Create completed assignment
        Assignment.objects.create(
            title='Completed HW',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            status='completed',
            user=user
        )
        
        # Create pending assignment
        Assignment.objects.create(
            title='Pending HW',
            course=course,
            due_date=timezone.now() + timedelta(days=14),
            status='not_started',
            user=user
        )
        
        assert course.pending_assignments() == 1

    def test_course_unique_together(self, user):
        """Test that course_code and user combination is unique."""
        Course.objects.create(
            course_code='MATH101',
            course_name='Calculus I',
            user=user
        )
        
        # Creating another course with same code and user should fail
        with pytest.raises(Exception):
            Course.objects.create(
                course_code='MATH101',
                course_name='Different Name',
                user=user
            )

    def test_course_ordering(self, user):
        """Test that courses are ordered by course_code."""
        Course.objects.create(course_code='CS201', course_name='Data Structures', user=user)
        Course.objects.create(course_code='CS101', course_name='Intro to CS', user=user)
        Course.objects.create(course_code='MATH101', course_name='Calculus', user=user)
        
        courses = list(Course.objects.filter(user=user))
        assert courses[0].course_code == 'CS101'
        assert courses[1].course_code == 'CS201'
        assert courses[2].course_code == 'MATH101'

    def test_course_color_choices(self, user):
        """Test that course can be created with different colors."""
        colors = ['#00274c', '#CC0000', '#0077b6', '#2a9d8f']
        for i, color in enumerate(colors):
            course = Course.objects.create(
                course_code=f'TEST{i}',
                course_name=f'Test Course {i}',
                color=color,
                user=user
            )
            assert course.color == color

    def test_course_cascade_delete(self, course, user):
        """Test that deleting a course deletes its assignments."""
        Assignment.objects.create(
            title='Test Assignment',
            course=course,
            due_date=timezone.now() + timedelta(days=7),
            user=user
        )
        
        assignment_count = Assignment.objects.filter(course=course).count()
        assert assignment_count == 1
        
        course.delete()
        
        # Assignments should be deleted with the course
        assignment_count = Assignment.objects.filter(course=course).count()
        assert assignment_count == 0
