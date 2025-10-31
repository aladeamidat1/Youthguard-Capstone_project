from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import UserProfile, Company

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_facilitator)
        self.assertFalse(user.is_employer)

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_profile(self):
        profile = UserProfile.objects.create(
            user=self.user,
            location='Lagos, Nigeria',
            skills='Python, Django',
            experience_level='intermediate'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.location, 'Lagos, Nigeria')

class AuthAPITest(APITestCase):
    def test_user_registration(self):
        url = reverse('create-user')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '08012345678'
        }
        response = self.client.post(url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
