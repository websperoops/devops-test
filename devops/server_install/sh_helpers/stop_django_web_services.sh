echo "INFO: Daemon reload"
systemctl daemon-reload

# Note: The order is important

echo "INFO: Stopping nginx"
systemctl stop nginx

echo "INFO: Stopping gunicorn"
systemctl stop gunicorn

echo "INFO: Stopping celeryflower"
systemctl stop celeryflower

echo "INFO: Stopping celerybeat"
systemctl stop celerybeat

echo "INFO: Stopping celery"
systemctl stop celery

echo "INFO: Stopping rabbitmq-server"
systemctl stop rabbitmq-server
