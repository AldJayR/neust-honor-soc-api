from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CampusViewSet,
    DepartmentViewSet,
    CourseViewSet,
    StudentViewSet,
    GWARecordViewSet,
    HonorSocietyOfficerViewSet,
    login_view,
    logout_view,
    token_refresh_view,
    user_profile
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'campuses', CampusViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'gwa-records', GWARecordViewSet)
router.register(r'officers', HonorSocietyOfficerViewSet)

urlpatterns = [
    # Custom Authentication endpoints (Honor Society specific)
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/refresh/', token_refresh_view, name='token_refresh'),
    path('auth/profile/', user_profile, name='user_profile'),
    
    # API endpoints
    path('', include(router.urls)),
]
