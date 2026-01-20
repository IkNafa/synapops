from django.db import models

class EnvironmentMode(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(to='users.Organization', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class Environment(models.Model):
    name = models.CharField(max_length=100)
    server = models.ForeignKey(to='servers.Server', on_delete=models.CASCADE, related_name='environments')
    mode = models.ForeignKey(to=EnvironmentMode, on_delete=models.CASCADE, related_name='environments')
    type = models.CharField(max_length=100)
    project = models.ForeignKey(to='environments.Project', on_delete=models.CASCADE, related_name='environments', null=True, blank=True)
    systemd_service_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name