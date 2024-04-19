"""
URL configuration for django_app project.
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Catch-all view to serve react application
    path('', TemplateView.as_view(template_name='index.html')),
]
