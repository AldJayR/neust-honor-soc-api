from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Campus, Department, Course, Student, GWARecord, HonorSocietyOfficer

class ModelTestCase(TestCase):
    def setUp(self):
        self.campus = Campus.objects.create(name="Main Campus", code="MAIN")
        self.department = Department.objects.create(
            name="Computer Science", 
            code="CS", 
            campus=self.campus
        )
        self.course = Course.objects.create(
            name="Bachelor of Science in Computer Science",
            code="BSCS",
            department=self.department
        )
        self.student = Student.objects.create(
            student_number="2024-001",
            first_name="John",
            last_name="Doe",
            campus=self.campus,
            year_level=1,
            department=self.department
        )
        self.user = User.objects.create_user(
            username="admin",
            password="testpass123"
        )
        self.officer = HonorSocietyOfficer.objects.create(
            user=self.user,
            position="President",
            campus=self.campus
        )

    def test_campus_creation(self):
        self.assertEqual(str(self.campus), "Main Campus")

    def test_student_creation(self):
        self.assertEqual(str(self.student), "John Doe (2024-001)")

    def test_officer_creation(self):
        self.assertTrue(self.officer.is_active)
        self.assertEqual(str(self.officer), "admin - President (Main Campus)")

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.campus = Campus.objects.create(name="Main Campus", code="MAIN")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.officer = HonorSocietyOfficer.objects.create(
            user=self.user,
            position="Secretary",
            campus=self.campus
        )

    def test_login_success(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_non_officer(self):
        # Create a user who is not an officer
        non_officer = User.objects.create_user(
            username="nonofficer",
            password="testpass123"
        )
        url = reverse('login')
        data = {
            'username': 'nonofficer',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
