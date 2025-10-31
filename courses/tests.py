from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Course, CourseEnrollment

User = get_user_model()

class CourseModelTest(TestCase):
    def setUp(self):
        self.facilitator = User.objects.create_user(
            username='facilitator',
            email='facilitator@example.com',
            password='testpass123',
            is_facilitator=True
        )

    def test_create_course(self):
        course = Course.objects.create(
            name='Python Basics',
            description='Learn Python programming fundamentals',
            facilitator=self.facilitator
        )
        self.assertEqual(course.name, 'Python Basics')
        self.assertEqual(course.facilitator, self.facilitator)
        self.assertFalse(course.is_approved)

class CourseEnrollmentTest(TestCase):
    def setUp(self):
        self.facilitator = User.objects.create_user(
            username='facilitator',
            email='facilitator@example.com',
            password='testpass123',
            is_facilitator=True
        )
        self.learner = User.objects.create_user(
            username='learner',
            email='learner@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Python Basics',
            description='Learn Python programming fundamentals',
            facilitator=self.facilitator,
            is_approved=True
        )

    def test_course_enrollment(self):
        enrollment = CourseEnrollment.objects.create(
            course=self.course,
            learner=self.learner
        )
        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(enrollment.learner, self.learner)
        self.assertEqual(enrollment.progress, 0)
        self.assertFalse(enrollment.completed)
