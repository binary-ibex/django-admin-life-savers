import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'custom_object_tool_button.settings')

application = get_wsgi_application()
