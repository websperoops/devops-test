echo "INFO: Daemon reload"
systemctl daemon-reload

# Note: The order of commands is important

echo "INFO: Stopping nginx"
systemctl stop nginx

echo "INFO: Stopping gunicorn"
systemctl stop gunicorn
# if there are problems with /run/gunicorn/socket, it needs to be done by 'service stop/start'
#service gunicorn stop

echo "INFO: Stopping celeryflower"
systemctl stop celeryflower

echo "INFO: Stopping celerybeat"
systemctl stop celerybeat

echo "INFO: Stopping celery"
systemctl stop celery

echo "INFO: Stopping rabbitmq-server"
systemctl stop rabbitmq-server

echo "INFO: Starting rabbitmq-server"
systemctl start rabbitmq-server

echo "INFO: Starting celery"
systemctl start celery

echo "INFO: Starting celerybeat"
systemctl start celerybeat

echo "INFO: Starting celeryflower"
systemctl start celeryflower

echo "INFO: Starting gunicorn"
systemctl start gunicorn
#service gunicorn start

echo "INFO: Starting nginx"
systemctl start nginx
