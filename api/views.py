from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .models import Campus, Department, Course, Student, GWARecord, HonorSocietyOfficer
from .serializers import (
    CampusSerializer,
    DepartmentSerializer,
    CourseSerializer,
    StudentSerializer,
    GWARecordSerializer,
    HonorSocietyOfficerSerializer,
    UserSerializer
)
from django.utils import timezone

# Create your views here.

# JWT Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not (username and password):
        return Response({'error': 'Username and password are required.'}, status=400)

    user = authenticate(request, username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials.'}, status=401)

    try:
        member = HonorSocietyOfficer.objects.get(user=user)
    except HonorSocietyOfficer.DoesNotExist:
        return Response({'error': 'User is not an officer.'}, status=403)

    if not member.is_active:
        return Response({'error': 'User is not an active officer.'}, status=403)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data,
        'member': HonorSocietyOfficerSerializer(member).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout by blacklisting the refresh token"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out.'}, status=200)
        return Response({'error': 'Refresh token is required.'}, status=400)
    except Exception as e:
        return Response({'error': 'Invalid token.'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    """Refresh access token using refresh token"""
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=400)
        
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token),
        })
    except Exception as e:
        return Response({'error': 'Invalid refresh token.'}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        member = HonorSocietyOfficer.objects.get(user=request.user)
        return Response({
            'user': UserSerializer(request.user).data,
            'member': HonorSocietyOfficerSerializer(member).data
        })
    except HonorSocietyOfficer.DoesNotExist:
        return Response({'error': 'User is not an officer.'}, status=403)

# CRUD ViewSets

class BaseViewSet(viewsets.ModelViewSet):
    """Base ViewSet with common functionality"""
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

class CampusViewSet(BaseViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    ordering = ['name']

class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name', 'code', 'campus__name']
    ordering_fields = ['name', 'code', 'campus__name']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        campus_id = self.request.query_params.get('campus')
        return queryset.filter(campus_id=campus_id) if campus_id else queryset

class CourseViewSet(BaseViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    search_fields = ['name', 'code', 'department__name']
    ordering_fields = ['name', 'code', 'department__name']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get('department')
        return queryset.filter(department_id=department_id) if department_id else queryset

class StudentViewSet(BaseViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    search_fields = ['student_number', 'first_name', 'last_name', 'campus__name', 'department__name']
    ordering_fields = ['student_number', 'first_name', 'last_name', 'year_level']
    ordering = ['last_name', 'first_name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {}
        
        # Build filter dictionary dynamically
        for param in ['campus', 'department', 'year_level']:
            value = self.request.query_params.get(param)
            if value:
                filter_key = f'{param}_id' if param in ['campus', 'department'] else param
                filters[filter_key] = value
        
        return queryset.filter(**filters) if filters else queryset

class GWARecordViewSet(BaseViewSet):
    queryset = GWARecord.objects.all()
    serializer_class = GWARecordSerializer
    search_fields = ['student__student_number', 'student__first_name', 'student__last_name', 'semester', 'academic_year']
    ordering_fields = ['academic_year', 'semester', 'gwa', 'created_at']
    ordering = ['-academic_year', '-semester']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {}
        
        # Standard filters
        for param in ['student', 'semester', 'academic_year']:
            value = self.request.query_params.get(param)
            if value:
                filter_key = f'{param}_id' if param == 'student' else param
                filters[filter_key] = value
        
        # GWA range filters
        min_gwa = self.request.query_params.get('min_gwa')
        max_gwa = self.request.query_params.get('max_gwa')
        
        if min_gwa:
            filters['gwa__gte'] = min_gwa
        if max_gwa:
            filters['gwa__lte'] = max_gwa
        
        return queryset.filter(**filters) if filters else queryset
    
    def perform_create(self, serializer):
        serializer.save(encoded_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(encoded_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def honor_eligible(self, request):
        """Get students eligible for honor society based on GWA"""
        min_gwa = request.query_params.get('min_gwa', '1.75')
        academic_year = request.query_params.get('academic_year')
        
        queryset = self.get_queryset()
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        honor_records = queryset.filter(gwa__lte=min_gwa)
        serializer = self.get_serializer(honor_records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get GWA statistics"""
        from django.db.models import Avg, Count, Max, Min
        
        queryset = self.get_queryset()
        academic_year = request.query_params.get('academic_year')
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        stats = queryset.aggregate(
            total_records=Count('id'),
            average_gwa=Avg('gwa'),
            highest_gwa=Min('gwa'),  # Lower GWA is better
            lowest_gwa=Max('gwa'),
            honor_eligible=Count('id', filter=models.Q(gwa__lte=1.75))
        )
        
        return Response(stats)

class HonorSocietyOfficerViewSet(BaseViewSet):
    queryset = HonorSocietyOfficer.objects.all()
    serializer_class = HonorSocietyOfficerSerializer
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'position', 'campus__name']
    ordering_fields = ['position', 'campus__name', 'is_active']
    ordering = ['position']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {}
        
        campus_id = self.request.query_params.get('campus')
        if campus_id:
            filters['campus_id'] = campus_id
            
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            filters['is_active'] = is_active.lower() == 'true'
        
        return queryset.filter(**filters) if filters else queryset

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register a new honor society officer"""
    # Extract user data
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    
    # Extract officer data
    position = request.data.get('position')
    campus_id = request.data.get('campus_id')
    
    # Validate required fields
    if not all([username, password, position, campus_id]):
        return Response({
            'error': 'Username, password, position, and campus_id are required.'
        }, status=400)
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=400)
    
    # Validate campus exists
    try:
        campus = Campus.objects.get(id=campus_id)
    except Campus.DoesNotExist:
        return Response({'error': 'Invalid campus ID.'}, status=400)
    
    try:
        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email or '',
            first_name=first_name or '',
            last_name=last_name or ''
        )
        
        # Create honor society officer
        officer = HonorSocietyOfficer.objects.create(
            user=user,
            position=position,
            campus=campus,
            is_active=True
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Officer registered successfully.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
            'officer': HonorSocietyOfficerSerializer(officer).data
        }, status=201)
        
    except Exception as e:
        # If officer creation fails, clean up the user
        if 'user' in locals():
            user.delete()
        return Response({'error': 'Registration failed. Please try again.'}, status=500)

