rabbitmqctl list_queues | awk '{ print $1 }' | xargs -L1 rabbitmqctl purge_queue
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app
