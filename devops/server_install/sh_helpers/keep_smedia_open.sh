#!/bin/sh
inotifywait -m -r -e create --format '%w%f' "/home/django/django_project/smedia/" | while read NEWFILE
do
	chmod -R 777 "/home/django/django_project/smedia/"
done
