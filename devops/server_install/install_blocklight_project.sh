#!/bin/bash
set -e

apt-get -y update
apt-get -y upgrade

# Create 'django' user if don't exists
if [ -z $(grep '^django' /etc/passwd) ]; then
  echo "Creating user: django"
  useradd -s /bin/bash -m django
  groupadd celery
  usermod -aG sudo -aG celery django
  mkdir /home/django/.ssh/
  cp /root/.ssh/authorized_keys /home/django/.ssh/
  echo "Set password for user: django"
  passwd django
fi

apt-get -y install python python-pip python3-pip nodejs virtualenv mysql-server rabbitmq-server nginx libmysqlclient-dev

if ! [ -e /home/django/django_project/ ]; then
  git clone https://github.com/jdarnold11/django_project.git /home/django/django_project/
  chown django:django -R /home/django/django_project/
else
  echo "/home/django/django_project already exists. Skipping git clone."
fi

virtualenv --python=python3.6 /home/django/bl_venv_python3.6

/home/django/bl_venv_python3.6/bin/pip install -r /home/django/django_project/requirements.txt
# currently need to install this additionaly of requiremets.txt until it will be fixed
/home/django/bl_venv_python3.6/bin/pip install pymysql flower


pushd /home/django/django_project/layout/src_react/
npm install
npm run build
popd

pushd /home/django/django_project/
/home/django/bl_venv_python3.6/bin/python manage.py collectstatic
popd

cp /root/server_install/etc/systemd/system/* /etc/systemd/system/
cp /root/server_install/lib/systemd/system/* /lib/systemd/system/
mkdir /etc/celery/
cp /root/server_install/etc/celery/celery.env /etc/celery/
cp -r /root/server_install/sh_helpers/ /root/
chmod u+x /root/sh_helpers/*

if [ -e /etc/nginx/sites-enabled/default ]; then
  rm /etc/nginx/sites-enabled/default
fi
cp /root/server_install/etc/nginx/sites-available/* /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/django_project \
      /etc/nginx/sites-enabled/django_project

mkdir /var/run/celery/
mkdir /var/log/celery/
chown :celery /var/run/celery
chown :celery /var/log/celery
chmod g+w /var/run/celery
chmod g+w /var/log/celery

echo "Next steps you need to do:"
echo "Checkout branch you want to deploy"
echo "Copy ssl files into /home/django/ssl/"
echo "Copy htpasswd file (used for authentication to flower) to /home/django/htpasswd"
echo "Setup Database"
echo "run ./sh_helpers/start_django_web_services.sh"
echo "You can check status of all installer servises by ./sh_helpers/show_django_web_services_status.sh"
