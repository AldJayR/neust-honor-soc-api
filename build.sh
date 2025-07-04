#!/bin/bash

# Production deployment script for Honor Society API

echo "🚀 Starting Honor Society API deployment..."
echo "==========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Load environment variables
if [ -f .env ]; then
    echo "📋 Loading environment variables..."
    export $(cat .env | grep -v '#' | xargs)
else
    echo "⚠️  No .env file found. Using default settings."
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations api
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Setting up admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from api.models import Campus, HonorSocietyOfficer

# Run tests to ensure everything works
echo "🧪 Running tests..."
python -m pytest -v --ds=honor_system.settings

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment completed successfully!"
    echo "========================================="
    echo "🔗 Next steps:"
    echo "   - Change the default admin password: admin/changeme123"
    echo "   - Set up your production database in .env"
    echo "   - Configure your web server (nginx/apache)"
    echo "   - Set up SSL certificates"
    echo "   - Review and update Django settings for production"
    echo ""
    echo "🌐 API Endpoints available at:"
    echo "   - /api/auth/login/     - Officer login"
    echo "   - /api/auth/register/  - Officer registration"
    echo "   - /api/campuses/       - Campus management"
    echo "   - /api/students/       - Student management"
    echo "   - /api/gwa-records/    - GWA record management"
    echo "   - /admin/              - Django admin interface"
else
    echo ""
    echo "❌ Deployment failed! Tests did not pass."
    echo "Please check the test output above and fix any issues."
    exit 1
fi
