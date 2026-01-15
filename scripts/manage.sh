# development server
python manage.py runserver

# Create app
python manage.py startapp tracker

# Create migrations
python manage.py makemigrations tracker

# Apply migrations
python manage.py migrate

# Check migrations
python manage.py sqlmigrate tracker 0001
python manage.py check

python manage.py shell

# Create admin user
python manage.py createsuperuser

# Test app
python manage.py test tracker
