python manage.py makemigrations
python manage.py makemigrations both
python manage.py migrate
nohup python manage.py runserver 0.0.0.0:8000
nohup python manage.py redis-server
nohup python manage.py celery -A both beat -l info -S django
nohup python manage.py celery worker -A both -l info
