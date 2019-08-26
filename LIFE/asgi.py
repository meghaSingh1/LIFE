import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LIFE.settings")
django.setup()
application = get_default_application()