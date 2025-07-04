from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Campus, Department, GWARecord, HonorSocietyOfficer, Course, Student

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'name', 'code']

class DepartmentSerializer(serializers.ModelSerializer):
    campus = CampusSerializer()

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'campus']

class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'department']

class StudentSerializer(serializers.ModelSerializer):
    campus = CampusSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Student
        fields = ['id', 'student_number', 'first_name', 'last_name', 'campus', 'year_level', 'department']  

class GWARecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    encoded_by = serializers.StringRelatedField()

    class Meta:
        model = GWARecord
        fields = ['id', 'student', 'semester', 'academic_year', 'gwa', 'encoded_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class HonorSocietyOfficerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    campus = CampusSerializer()

    class Meta:
        model = HonorSocietyOfficer
        fields = ['id', 'user', 'position', 'campus', 'is_active']
        read_only_fields = ['is_active']
