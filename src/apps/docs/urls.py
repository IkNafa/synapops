from django.urls import path

from .views import api_documentation

urlpatterns = [
    path('', api_documentation, name='api-documentation'),
]
