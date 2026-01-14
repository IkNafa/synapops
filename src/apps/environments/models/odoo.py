from django.db import models

from .mixins import EnvironmentMixin

class OdooEnvironment(EnvironmentMixin):
    REQUIRED_ENVIRONMENT_TYPE = 'odoo'

    version = models.CharField(max_length=20)
    is_enterprise = models.BooleanField(default=False)
    python_version = models.CharField(max_length=10)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.environment.name} - {self.environment.mode.name} ({self.version})"
    
    def get_config_parameter(self, key, default=None):
        try:
            config = self.configurations.get(key=key)
            return config.value
        except OdooConfiguration.DoesNotExist:
            return default

class OdooDatabase(models.Model):
    environment = models.ForeignKey(to=OdooEnvironment, on_delete=models.CASCADE, related_name='databases')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.environment.environment.name})"

class OdooConfiguration(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    environment = models.ForeignKey(to=OdooEnvironment, on_delete=models.CASCADE, related_name='configurations')

class OdooPath(models.Model):
    PATH_TYPES = [
        ('core', 'Core'),
        ('config', 'Config'),
        ('addons', 'Addons'),
        ('python', 'Python'),
    ]
    environment = models.ForeignKey(to=OdooEnvironment, on_delete=models.CASCADE, related_name='paths')
    path_type = models.CharField(max_length=10, choices=PATH_TYPES)
    path = models.CharField(max_length=200)

    own_addons = models.BooleanField(default=False)
    oca_addons = models.BooleanField(default=False)
    store_addons = models.BooleanField(default=False)
    other_addons = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.path} ({self.environment.environment.name})"
