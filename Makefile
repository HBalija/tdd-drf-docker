build:
	docker-compose build

migrations:
	  docker-compose run --rm app sh -c "python manage.py makemigrations && python manage.py migrate"

test:
	docker-compose run --rm app sh -c "python manage.py test && flake8"

up-build:
	docker-compose up --build

up:
	docker-compose up
