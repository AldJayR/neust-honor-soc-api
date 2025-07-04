#!/usr/bin/env python
"""
Test runner for Honor Society API using pytest
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'honor_system.settings')
    django.setup()
    
    import pytest
    
    # Run pytest with coverage and verbose output
    exit_code = pytest.main([
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        '--cov=api',  # Coverage for api app
        '--cov-report=term-missing',  # Show missing lines
        '--cov-report=html',  # Generate HTML coverage report
        '--strict-markers',  # Strict marker checking
        'api/tests/',  # Test directory
    ])
    
    sys.exit(exit_code)
