from django.db import models
from django.forms import ValidationError

from .mixins import EnvironmentMixin

class DockerEnvironment(EnvironmentMixin):
    REQUIRED_ENVIRONMENT_TYPE = 'docker'

    compose_file_path = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.environment.name} - {self.environment.mode.name}"
    
class DockerService(models.Model):
    environment = models.ForeignKey(to=DockerEnvironment, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)

    build_context = models.CharField(max_length=200, blank=True, null=True)
    dockerfile_path = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    tag = models.CharField(max_length=50, blank=True, null=True)
    command = models.CharField(max_length=200, blank=True, null=True)
    
    ports = models.JSONField(blank=True, null=True)
    volumes = models.JSONField(blank=True, null=True)
    environment_variables = models.JSONField(blank=True, null=True)

    depends_on = models.ManyToManyField(to='self', symmetrical=False, blank=True, related_name='dependents')

    def __str__(self):
        name = f"{self.name}"
        if self.image:
            name += f" ({self.image}:{self.tag or 'latest'})"
        return name