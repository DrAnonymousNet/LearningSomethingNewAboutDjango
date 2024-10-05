# wsgi.py (same logic applies to asgi.py)

import os
from django.core.wsgi import get_wsgi_application
from your_project.settings import start_queue_listener

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

start_queue_listener()  # Start async log listener

application = get_wsgi_application()