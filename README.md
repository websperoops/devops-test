
# Blocklight Dashboard 0.1b #

## About ##
This app is the codebase for the Blocklight Analytics App

```
Django 2.2
python3
MYSQL 8.3
MySQL Workbench or Similar
RabbitMQ 3.6 - https://www.rabbitmq.com/download.html
nodejs
```
This project is ongoing and proprietary.

## Quick Install or Setup project in you local ##

$ mkdir blocklight                                                      # Create the project folder
$ cd blocklight
$ virtualenv venv                                                       # Create virtual environment to run the project locally
$ git clone git@github.com:jdarnold11/blocklight.git                    # Clone the repo ** SSH Authentication Required **
$ source venv/bin/activate                                              # Start virtual environment
$ cd blocklight/custom-libs/
$ rm -r django-allauth-blocklight                                       # Remove the empty submodule repo
$ git clone git@github.com:awaris123/django-allauth-blocklight.git      # Clone the submodule repo ** SSH Authentication Required **
$ cd ..
$ pip3 install -r requirements.txt                                      # Install the requirements from the requirements.txt file
$ [MySQL Workbench (or similar)] import blocklightx database            # File is from Google Drive > 0.1 Development > 0.2 Database
$ service mysql start
$ set -a
$ . env_localhost (You'll be provided this file - update db user/pw)    # Set the local environment
$ set +a
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ pushd layout/src_react/
$ npm install
$ npm run build
$ python3 manage.py collectstatic --noinput
$ python3 manage.py runserver                                           # Run the server

[open 2nd terminal]
$ cd blocklight
$ source venv/bin/activate                                              # Start virtual environment
$ cd blocklight
$ set -a
$ . env_localhost                                                       # Set the local environment
$ set +a
$ celery -A blocklight -l info worker                                   # Start celery worker

[open 3rd terminal]
$ cd blocklight
$ source venv/bin/activate                                              # Start virtual environment
$ cd blocklight
$ set -a
$ . env_localhost                                                       # Set the local environment
$ set +a
$ celery -A blocklight -l info beat                                     # Start celery beat

