import pytest
from rest_framework import status
from django.contrib.auth.models import User


@pytest.mark.integration
class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_login_success(self, api_client, honor_society_officer):
        """Test successful login"""
        url = '/api/auth/login/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data
        assert 'member' in response.data
    
    def test_login_invalid_credentials(self, api_client, honor_society_officer):
        """Test login with invalid credentials"""
        url = '/api/auth/login/'
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data
    
    def test_login_missing_credentials(self, api_client):
        """Test login with missing credentials"""
        url = '/api/auth/login/'
        
        # Missing password
        response = api_client.post(url, {'username': 'testuser'}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Missing username
        response = api_client.post(url, {'password': 'testpass123'}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Missing both
        response = api_client.post(url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_login_non_officer(self, api_client, campus):
        """Test login with user who is not an officer"""
        # Create a user who is not an officer
        non_officer = User.objects.create_user(
            username="nonofficer",
            password="testpass123"
        )
        
        url = '/api/auth/login/'
        data = {
            'username': 'nonofficer',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'error' in response.data
    
    def test_login_inactive_officer(self, api_client, user, campus):
        """Test login with inactive officer"""
        # Create inactive officer
        from api.models import HonorSocietyOfficer
        inactive_officer = HonorSocietyOfficer.objects.create(
            user=user,
            position="Inactive Officer",
            campus=campus,
            is_active=False
        )
        
        url = '/api/auth/login/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'error' in response.data
    
    def test_login_unverified_officer(self, api_client, user, campus):
        """Test login with unverified officer"""
        # Create unverified officer
        from api.models import HonorSocietyOfficer
        unverified_officer = HonorSocietyOfficer.objects.create(
            user=user,
            position="Unverified Officer",
            campus=campus,
            is_active=True,
            is_verified=False
        )
        
        url = '/api/auth/login/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'verification' in response.data['error']
    
    def test_user_profile(self, authenticated_client):
        """Test user profile endpoint"""
        url = '/api/auth/profile/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'user' in response.data
        assert 'member' in response.data
    
    def test_user_profile_unauthenticated(self, unauthenticated_client):
        """Test user profile endpoint without authentication"""
        url = '/api/auth/profile/'
        response = unauthenticated_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_endpoints(self, api_client, honor_society_officer):
        """Test standard JWT token endpoints"""
        # Test token obtain
        url = '/api/token/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        
        # Test token refresh
        refresh_token = response.data['refresh']
        refresh_url = '/api/token/refresh/'
        refresh_data = {'refresh': refresh_token}
        refresh_response = api_client.post(refresh_url, refresh_data, format='json')
        
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data
        
        # Test token verify
        access_token = response.data['access']
        verify_url = '/api/token/verify/'
        verify_data = {'token': access_token}
        verify_response = api_client.post(verify_url, verify_data, format='json')
        
        assert verify_response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_register_success(self, api_client, campus):
        """Test successful officer registration"""
        url = '/api/auth/register/'
        data = {
            'username': 'newofficer',
            'password': 'newpass123',
            'email': 'newofficer@example.com',
            'first_name': 'New',
            'last_name': 'Officer',
            'position': 'Secretary',
            'campus_id': campus.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        # No tokens should be returned since user needs verification
        assert 'access' not in response.data
        assert 'refresh' not in response.data
        assert response.data['user']['username'] == 'newofficer'
        assert response.data['officer']['position'] == 'Secretary'
        assert response.data['officer']['is_verified'] == False
        assert 'verification' in response.data['message']
    
    @pytest.mark.django_db
    def test_register_duplicate_username(self, api_client, campus):
        """Test registration with existing username"""
        # Create a user first
        from django.contrib.auth.models import User
        User.objects.create_user(username='existinguser', password='pass123')
        
        url = '/api/auth/register/'
        data = {
            'username': 'existinguser',
            'password': 'newpass123',
            'position': 'Treasurer',
            'campus_id': campus.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Username already exists' in response.data['error']
    
    @pytest.mark.django_db
    def test_register_missing_fields(self, api_client):
        """Test registration with missing required fields"""
        url = '/api/auth/register/'
        data = {'username': 'incomplete'}
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'required' in response.data['error']
    
    @pytest.mark.django_db
    def test_register_invalid_campus(self, api_client):
        """Test registration with invalid campus ID"""
        url = '/api/auth/register/'
        data = {
            'username': 'testuser2',
            'password': 'testpass123',
            'position': 'Vice President',
            'campus_id': 99999  # Non-existent campus
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Invalid campus ID' in response.data['error']
