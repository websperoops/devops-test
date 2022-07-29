set -e

if [ -z $BLOCKLIGHT_ENV_TO_DEPLOY ]; then
  echo "You need to set branch you want to deploy in env variable BLOCKLIGHT_ENV_TO_DEPLOY"
  echo "Usually 'development' or 'production'"
  echo "You can put it into ~/.bashrc file (export BLOCKLIGHT_ENV_TO_DEPLOY=...) to load it automatically"
  exit 1
fi

PYTHON_VENV_BIN=/home/django/bl_venv_python3.6/bin/python
PYTHON_VENV_PIP=/home/django/bl_venv_python3.6/bin/pip
DJANGO_PROJECT=/home/django/django_project/

su - django -c "cd $DJANGO_PROJECT; git stash"
su - django -c "cd $DJANGO_PROJECT; git checkout $BLOCKLIGHT_ENV_TO_DEPLOY"
su - django -c "cd $DJANGO_PROJECT; git pull"
su - django -c "cd $DJANGO_PROJECT; git submodule update --init --recursive"
su - django -c "cd $DJANGO_PROJECT; $PYTHON_VENV_PIP install -r requirements.txt"
su - django -c "cd $DJANGO_PROJECT/layout/src_react/; npm install"
su - django -c "cd $DJANGO_PROJECT/layout/src_react/; npm run build"
su - django -c "cd $DJANGO_PROJECT; set -a; . .env; set +a; $PYTHON_VENV_BIN /home/django/django_project/manage.py collectstatic --no-input"

. /root/sh_helpers/restart_django_web_services.sh

echo "Newest changes in '$BLOCKLIGHT_ENV_TO_DEPLOY' were deployed."
