import pytest
from rest_framework import status


@pytest.mark.integration
class TestCampusAPI:
    """Test Campus CRUD operations"""
    
    def test_create_campus(self, authenticated_client):
        """Test creating a new campus"""
        url = '/api/campuses/'
        data = {'name': 'New Campus', 'code': 'NEW'}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Campus'
        assert response.data['code'] == 'NEW'
    
    def test_list_campuses(self, authenticated_client, campus):
        """Test listing campuses"""
        url = '/api/campuses/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) >= 1
    
    def test_retrieve_campus(self, authenticated_client, campus):
        """Test retrieving a specific campus"""
        url = f'/api/campuses/{campus.id}/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == campus.name
        assert response.data['code'] == campus.code
    
    def test_update_campus(self, authenticated_client, campus):
        """Test updating a campus"""
        url = f'/api/campuses/{campus.id}/'
        data = {'name': 'Updated Campus', 'code': 'UPD'}
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Campus'
        assert response.data['code'] == 'UPD'
    
    def test_partial_update_campus(self, authenticated_client, campus):
        """Test partially updating a campus"""
        url = f'/api/campuses/{campus.id}/'
        data = {'name': 'Partially Updated Campus'}
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Partially Updated Campus'
        assert response.data['code'] == campus.code  # Should remain unchanged
    
    def test_delete_campus(self, authenticated_client, campus):
        """Test deleting a campus"""
        url = f'/api/campuses/{campus.id}/'
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        get_response = authenticated_client.get(url)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_search_campuses(self, authenticated_client, campus):
        """Test searching campuses"""
        url = '/api/campuses/?search=Test'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
    
    def test_order_campuses(self, authenticated_client, campus):
        """Test ordering campuses"""
        # Create another campus for ordering test
        from api.models import Campus
        Campus.objects.create(name='Another Campus', code='ANTH')
        
        url = '/api/campuses/?ordering=name'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 2
    
    def test_campus_unauthenticated_access(self, unauthenticated_client):
        """Test that unauthenticated users cannot access campus endpoints"""
        urls = [
            '/api/campuses/',
            '/api/campuses/1/',
        ]
        
        for url in urls:
            response = unauthenticated_client.get(url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestDepartmentAPI:
    """Test Department CRUD operations"""
    
    def test_create_department(self, authenticated_client, campus):
        """Test creating a new department"""
        url = '/api/departments/'
        data = {
            'name': 'New Department',
            'code': 'ND',
            'campus_id': campus.id
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Department'
        assert response.data['code'] == 'ND'
    
    def test_list_departments(self, authenticated_client, department):
        """Test listing departments"""
        url = '/api/departments/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) >= 1
    
    def test_filter_departments_by_campus(self, authenticated_client, department, campus):
        """Test filtering departments by campus"""
        url = f'/api/departments/?campus={campus.id}'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        for dept in response.data['results']:
            assert dept['campus']['id'] == campus.id
    
    def test_search_departments(self, authenticated_client, department):
        """Test searching departments"""
        url = '/api/departments/?search=Information'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Should find the CICT department
        assert len(response.data['results']) >= 1


@pytest.mark.integration  
class TestStudentAPI:
    """Test Student CRUD operations"""
    
    def test_create_student(self, authenticated_client, campus, department):
        """Test creating a new student"""
        url = '/api/students/'
        data = {
            'student_number': '2024-002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'campus_id': campus.id,
            'year_level': 2,
            'department_id': department.id
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['student_number'] == '2024-002'
        assert response.data['first_name'] == 'Jane'
        assert response.data['last_name'] == 'Smith'
    
    def test_list_students(self, authenticated_client, student):
        """Test listing students"""
        url = '/api/students/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) >= 1
    
    def test_filter_students(self, authenticated_client, student, campus, department):
        """Test filtering students by various criteria"""
        # Filter by campus
        url = f'/api/students/?campus={campus.id}'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
        # Filter by department
        url = f'/api/students/?department={department.id}'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
        # Filter by year level
        url = '/api/students/?year_level=1'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
class TestGWARecordAPI:
    """Test GWA Record CRUD operations"""
    
    def test_create_gwa_record(self, authenticated_client, student):
        """Test creating a new GWA record"""
        url = '/api/gwa-records/'
        data = {
            'student_id': student.id,
            'semester': '2nd Semester',
            'academic_year': '2024-2025',
            'gwa': 1.75
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['gwa'] == '1.75'
        assert response.data['semester'] == '2nd Semester'
    
    def test_list_gwa_records(self, authenticated_client, gwa_record):
        """Test listing GWA records"""
        url = '/api/gwa-records/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) >= 1
    
    def test_honor_eligible_endpoint(self, authenticated_client, gwa_record):
        """Test honor eligible students endpoint"""
        url = '/api/gwa-records/honor_eligible/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Should include our record with GWA 1.50 (honor eligible)
        assert len(response.data) >= 1
    
    def test_gwa_statistics_endpoint(self, authenticated_client, gwa_record):
        """Test GWA statistics endpoint"""
        url = '/api/gwa-records/statistics/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total_records' in response.data
        assert 'average_gwa' in response.data
        assert 'highest_gwa' in response.data
        assert 'lowest_gwa' in response.data
        assert 'honor_eligible' in response.data
