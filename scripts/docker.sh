docker build .

docker-compose up
docker-compose down

docker-compose up -d --build

docker-compose exec web python manage.py migrate
