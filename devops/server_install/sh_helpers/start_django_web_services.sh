echo "INFO: Daemon reload"
systemctl daemon-reload

# Note: The order is important

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

echo "INFO: Starting nginx"
systemctl start nginx
