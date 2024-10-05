# your_app/views.py

import logging
from django.shortcuts import render

logger = logging.getLogger('your_app')

def my_view(request):
    # Example log
    logger.info('User requested the homepage')
    logger.error('An error occurred while processing the request', extra={'password': 'supersecret'})

    return render(request, 'index.html')