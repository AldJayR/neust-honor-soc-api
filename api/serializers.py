from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Campus, Department, GWARecord, HonorSocietyOfficer, Course, Student

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'name', 'code']

class DepartmentSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(read_only=True)
    campus_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'campus', 'campus_id']

class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'department', 'department_id']

class StudentSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    campus_id = serializers.IntegerField(write_only=True)
    department_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Student
        fields = ['id', 'student_number', 'first_name', 'last_name', 'campus', 'year_level', 'department', 'campus_id', 'department_id']  

class GWARecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    encoded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GWARecord
        fields = ['id', 'student', 'semester', 'academic_year', 'gwa', 'encoded_by', 'created_at', 'updated_at', 'student_id']
        read_only_fields = ['created_at', 'updated_at', 'encoded_by']

    def create(self, validated_data):
        validated_data['encoded_by'] = self.context['request'].user
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class HonorSocietyOfficerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    campus = CampusSerializer()

    class Meta:
        model = HonorSocietyOfficer
        fields = ['id', 'user', 'position', 'campus', 'is_active', 'is_verified']
        read_only_fields = ['is_active', 'is_verified']
