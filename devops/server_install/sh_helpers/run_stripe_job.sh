set -e

PYTHON_VENV_BIN=/home/django/bl_venv_python3.6/bin/python
DJANGO_PROJECT=/home/django/django_project/

su - django -c "cd $DJANGO_PROJECT; set -a; . .env; set +a; $PYTHON_VENV_BIN /home/django/django_project/manage.py celery call execute_all_recurring_payments"
