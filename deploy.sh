#!/bin/bash

# Production deployment script for Honor Society API

echo "🚀 Starting Honor Society API deployment..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'changeme123')
    print('Superuser created: admin/changeme123')
else:
    print('Superuser already exists')
"

# Run tests
echo "🧪 Running tests..."
python manage.py test

echo "✅ Deployment completed successfully!"
echo "🔗 Don't forget to:"
echo "   - Change the default superuser password"
echo "   - Set up your production database"
echo "   - Configure your web server (nginx/apache)"
echo "   - Set up SSL certificates"
