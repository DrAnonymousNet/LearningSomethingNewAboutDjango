# your_app/middleware.py

import uuid
from django.utils.deprecation import MiddlewareMixin
from your_app.logging_filters import set_correlation_id

class CorrelationIdMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Generate a unique correlation ID for the request
        correlation_id = str(uuid.uuid4())
        set_correlation_id(correlation_id)
        request.correlation_id = correlation_id

    def process_response(self, request, response):
        # Add correlation ID to the response headers
        if hasattr(request, 'correlation_id'):
            response['X-Correlation-ID'] = request.correlation_id
        return response 