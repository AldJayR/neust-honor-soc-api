# Legacy tests.py file - pytest tests are now in api/tests/ directory
# This file is kept for backwards compatibility with Django's test discovery

# Import all pytest test classes to make them discoverable by Django's test runner
from .tests.test_models import TestModels
from .tests.test_authentication import TestAuthentication  
from .tests.test_api import TestCampusAPI, TestDepartmentAPI, TestStudentAPI, TestGWARecordAPI, TestHealthCheck

# Note: Run tests with pytest for better experience:
# pytest -v
# or
# python -m pytest -v
