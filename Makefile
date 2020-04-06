build:
	docker-compose build

migrations:
	  docker-compose run app sh -c "python manage.py makemigrations && python manage.py migrate"

test:
	docker-compose run app sh -c "python manage.py test && flake8"
