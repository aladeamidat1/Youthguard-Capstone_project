from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Job, JobApplication
from core.models import Company

User = get_user_model()

class JobModelTest(TestCase):
    def setUp(self):
        self.employer = User.objects.create_user(
            username='employer',
            email='employer@example.com',
            password='testpass123',
            is_employer=True
        )
        self.company = Company.objects.create(
            name='Tech Corp',
            description='A tech company',
            employer=self.employer
        )

    def test_create_job(self):
        job = Job.objects.create(
            company=self.company,
            title='Python Developer',
            description='We are looking for a Python developer'
        )
        self.assertEqual(job.title, 'Python Developer')
        self.assertEqual(job.company, self.company)
        self.assertFalse(job.is_approved)

class JobApplicationTest(TestCase):
    def setUp(self):
        self.employer = User.objects.create_user(
            username='employer',
            email='employer@example.com',
            password='testpass123',
            is_employer=True
        )
        self.applicant = User.objects.create_user(
            username='applicant',
            email='applicant@example.com',
            password='testpass123'
        )
        self.company = Company.objects.create(
            name='Tech Corp',
            description='A tech company',
            employer=self.employer
        )
        self.job = Job.objects.create(
            company=self.company,
            title='Python Developer',
            description='We are looking for a Python developer',
            is_approved=True
        )

    def test_job_application(self):
        application = JobApplication.objects.create(
            job=self.job,
            applicant=self.applicant,
            cover_letter='I am interested in this position'
        )
        self.assertEqual(application.job, self.job)
        self.assertEqual(application.applicant, self.applicant)
        self.assertEqual(application.status, 'pending')
