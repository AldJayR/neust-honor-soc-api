from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Campus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Student(models.Model):
    student_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    year_level = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_number})"
    
class GWARecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=10)
    gwa = models.DecimalField(max_digits=4, decimal_places=2)
    encoded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gwa_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'semester', 'academic_year')

    def __str__(self):
        return f"{self.student} - {self.semester} {self.academic_year}: {self.gwa}"
    
class HonorSocietyOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.position} ({self.campus.name})"