import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
# Ensure django is setup before any tests run
django.setup()
