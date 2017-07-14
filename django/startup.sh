redis-server &
python manage.py makemigrations
python manage.py makemigrations both
python manage.py migrate
nohup celery -A both beat -l info -S django &
nohup celery worker -A both -l info &
python manage.py runserver 0.0.0.0:8000

