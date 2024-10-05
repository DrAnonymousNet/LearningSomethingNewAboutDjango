# your_app/logging_filters.py

import logging
import re
from threading import local

# Thread-local storage for correlation ID
_log_context = local()

def set_correlation_id(correlation_id):
    _log_context.correlation_id = correlation_id

def get_correlation_id():
    return getattr(_log_context, 'correlation_id', 'unknown')


class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        # Add correlation_id to log record
        record.correlation_id = get_correlation_id()
        return True


class MaskSensitiveDataFilter(logging.Filter):
    SENSITIVE_FIELDS = ['password', 'api_key']

    def filter(self, record):
        # Mask sensitive fields
        for field in self.SENSITIVE_FIELDS:
            pattern = re.compile(rf'({field})=(\S+)', re.IGNORECASE)
            record.msg = pattern.sub(r'\1=******', record.msg)
        return True


class AddUserInfoFilter(logging.Filter):
    def filter(self, record):
        from django.utils.thread_support import current_request

        request = getattr(current_request(), 'request', None)
        if request and request.user.is_authenticated:
            record.user = f'{request.user.username} (ID: {request.user.id})'
        else:
            record.user = 'Anonymous'
        return True