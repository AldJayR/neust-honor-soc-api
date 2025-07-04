import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Provide an API client for making requests"""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user"""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123"
    )


@pytest.fixture
def campus(db):
    """Create a test campus"""
    from api.models import Campus
    return Campus.objects.create(
        name="Test Campus",
        code="TEST"
    )


@pytest.fixture
def department(db, campus):
    """Create a test department"""
    from api.models import Department
    return Department.objects.create(
        name="Computer Science",
        code="CS",
        campus=campus
    )


@pytest.fixture
def course(db, department):
    """Create a test course"""
    from api.models import Course
    return Course.objects.create(
        name="Bachelor of Science in Computer Science",
        code="BSCS",
        department=department
    )


@pytest.fixture
def student(db, campus, department):
    """Create a test student"""
    from api.models import Student
    return Student.objects.create(
        student_number="2024-001",
        first_name="John",
        last_name="Doe",
        campus=campus,
        year_level=1,
        department=department
    )


@pytest.fixture
def honor_society_officer(db, user, campus):
    """Create a test honor society officer"""
    from api.models import HonorSocietyOfficer
    return HonorSocietyOfficer.objects.create(
        user=user,
        position="President",
        campus=campus,
        is_active=True,
        is_verified=True  # Make sure the test officer is verified
    )


@pytest.fixture
def gwa_record(db, student, user):
    """Create a test GWA record"""
    from api.models import GWARecord
    return GWARecord.objects.create(
        student=student,
        semester="1st Semester",
        academic_year="2024-2025",
        gwa=1.50,
        encoded_by=user
    )


@pytest.fixture
def authenticated_client(api_client, user, honor_society_officer):
    """Provide an authenticated API client"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def unauthenticated_client(api_client):
    """Provide an unauthenticated API client"""
    return api_client
