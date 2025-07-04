#!/bin/bash

# Production deployment script for Honor Society API

echo "🚀 Starting Honor Society API deployment..."
echo "==========================================="

# Load environment variables from .env file
if [ -f .env ]; then
    echo "📋 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️  .env file not found, using default values"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt



# Create superuser if it doesn't exist
echo "👤 Creating Django superuser (if not exists)..."
if python manage.py createsuperuser --noinput \
    --username "${DJANGO_SUPERUSER_USERNAME:-admin}" \
    --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
    2>/dev/null; then
    echo "✅ Superuser created successfully"
else
    echo "ℹ️  Superuser already exists or creation was skipped"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Run tests to ensure everything works
echo "🧪 Running tests..."
python -m pytest -v --ds=honor_system.settings

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment completed successfully!"
    echo "========================================="
    echo "🔗 Next steps:"
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