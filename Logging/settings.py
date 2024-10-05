# settings.py

import os
from logging.handlers import RotatingFileHandler, QueueHandler
from queue import Queue
from pythonjsonlogger import jsonlogger

# Create directory for logs
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Create a queue for asynchronous logging
log_queue = Queue()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {
            '()': 'your_app.logging_filters.CorrelationIdFilter',
        },
        'mask_sensitive_data': {
            '()': 'your_app.logging_filters.MaskSensitiveDataFilter',
        },
        'user_info': {
            '()': 'your_app.logging_filters.AddUserInfoFilter',
        },
    },
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '[%(asctime)s] %(levelname)s %(correlation_id)s %(user)s %(message)s',
        },
        'verbose': {
            'format': '[{asctime}] {levelname} {correlation_id} {user} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'queue': {
            'class': 'logging.handlers.QueueHandler',
            'queue': log_queue,
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
            'filters': ['correlation_id', 'mask_sensitive_data', 'user_info'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'filters': ['correlation_id', 'user_info'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['queue'],  # Using asynchronous queue logging
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['queue'],  # Handle HTTP request logging
            'level': 'ERROR',
            'propagate': False,
        },
        'your_app': {
            'handlers': ['queue'],  # Use this logger for your app
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Start QueueListener to process logs asynchronously
def start_queue_listener():
    from logging.handlers import QueueListener
    listener = QueueListener(log_queue, logging.FileHandler(os.path.join(LOG_DIR, 'errors.log')), logging.StreamHandler())
    listener.start()