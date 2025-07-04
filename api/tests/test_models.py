import pytest
from api.models import Campus, Department, Course, Student, GWARecord, HonorSocietyOfficer


@pytest.mark.unit
class TestModels:
    """Test model functionality"""
    
    def test_campus_creation(self, campus):
        """Test campus model creation and string representation"""
        assert str(campus) == "Test Campus"
        assert campus.name == "Test Campus"
        assert campus.code == "TEST"
    
    def test_department_creation(self, department, campus):
        """Test department model creation and relationships"""
        assert str(department) == "Computer Science"
        assert department.campus == campus
        assert department.code == "CS"
    
    def test_course_creation(self, course, department):
        """Test course model creation"""
        assert str(course) == "Bachelor of Science in Computer Science (BSCS)"
        assert course.department == department
    
    def test_student_creation(self, student, campus, department):
        """Test student model creation"""
        assert str(student) == "John Doe (2024-001)"
        assert student.campus == campus
        assert student.department == department
        assert student.year_level == 1
    
    def test_honor_society_officer_creation(self, honor_society_officer, user, campus):
        """Test honor society officer model"""
        assert honor_society_officer.is_active is True
        assert str(honor_society_officer) == "testuser - President (Test Campus)"
        assert honor_society_officer.user == user
        assert honor_society_officer.campus == campus
    
    def test_gwa_record_creation(self, gwa_record, student, user):
        """Test GWA record model"""
        assert gwa_record.student == student
        assert gwa_record.encoded_by == user
        assert gwa_record.gwa == 1.50
        assert str(gwa_record) == "John Doe (2024-001) - 1st Semester 2024-2025: 1.50"
    
    def test_gwa_record_unique_constraint(self, student, user):
        """Test that GWA records have unique constraint on student, semester, academic_year"""
        # Create first record
        GWARecord.objects.create(
            student=student,
            semester="1st Semester", 
            academic_year="2024-2025",
            gwa=1.50,
            encoded_by=user
        )
        
        # Try to create duplicate - should raise error
        with pytest.raises(Exception):  # IntegrityError
            GWARecord.objects.create(
                student=student,
                semester="1st Semester",
                academic_year="2024-2025", 
                gwa=1.75,
                encoded_by=user
            )
