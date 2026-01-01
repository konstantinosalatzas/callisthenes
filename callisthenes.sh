# development server
python manage.py runserver

# Create app
python manage.py startapp training

# Create migrations
python manage.py makemigrations training

# Apply migrations
python manage.py migrate

python manage.py sqlmigrate training 0001
python manage.py check

python manage.py createsuperuser
