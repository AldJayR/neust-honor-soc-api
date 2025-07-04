from django.contrib import admin
from .models import Campus, Department, Course, Student, GWARecord, HonorSocietyOfficer

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'campus']
    list_filter = ['campus']
    search_fields = ['name', 'code', 'campus__name']
    ordering = ['campus__name', 'name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'get_campus']
    list_filter = ['department__campus', 'department']
    search_fields = ['name', 'code', 'department__name']
    ordering = ['department__campus__name', 'department__name', 'name']
    
    def get_campus(self, obj):
        return obj.department.campus.name
    get_campus.short_description = 'Campus'
    get_campus.admin_order_field = 'department__campus__name'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_number', 'first_name', 'last_name', 'campus', 'department', 'year_level']
    list_filter = ['campus', 'department', 'year_level']
    search_fields = ['student_number', 'first_name', 'last_name']
    ordering = ['last_name', 'first_name']

@admin.register(GWARecord)
class GWARecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'academic_year', 'gwa', 'encoded_by', 'created_at']
    list_filter = ['semester', 'academic_year', 'encoded_by']
    search_fields = ['student__student_number', 'student__first_name', 'student__last_name']
    ordering = ['-academic_year', '-semester', 'student__last_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(HonorSocietyOfficer)
class HonorSocietyOfficerAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'campus', 'is_active']
    list_filter = ['campus', 'position', 'is_active']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'position']
    ordering = ['campus__name', 'position']
