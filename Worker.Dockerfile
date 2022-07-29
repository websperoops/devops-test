FROM python:3
ENV PYTHONUNBUFFERED=1
SHELL ["/bin/bash", "-c", "-l"]
WORKDIR /blocklight/custom-libs/django-allauth-blocklight
COPY /custom-libs/django-allauth-blocklight/ /blocklight/custom-libs/django-allauth-blocklight/
RUN python setup.py install 
WORKDIR /blocklight
COPY requirements.txt /blocklight/
COPY /custom-libs/django-allauth-blocklight/ /blocklight/custom-libs/django-allauth-blocklight/
RUN pip install -r requirements.txt
RUN apt-get install libyaml-dev
COPY . /blocklight//