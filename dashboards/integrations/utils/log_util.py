from celery.app.log import TaskFormatter
from celery.utils.log import get_task_logger

import logging
import os


ROOT_LOG_PATH = "./integration_logs/"
LOG_PATH = ROOT_LOG_PATH + "{}_logs/"


def check_dir(integration_name):
    path = LOG_PATH.format(integration_name)

    if not os.path.isdir(ROOT_LOG_PATH):
        os.mkdir(ROOT_LOG_PATH)

    if not os.path.isdir(path):
        os.mkdir(path)

    return

def set_log_fh(logger, integration_name):
    fh = logging.handlers.RotatingFileHandler(LOG_PATH.format(integration_name) + "log")
    fh.setFormatter(TaskFormatter('%(asctime)s | %(task_id)s | %(task_name)s | %(name)s | %(levelname)s | %(message)s'))
    logger.addHandler(fh)

    return logger

def create_integration_logger(module, integration_name):
    logger = get_task_logger(module)
    check_dir(integration_name)
    return set_log_fh(logger, integration_name)
