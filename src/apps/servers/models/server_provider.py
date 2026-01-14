from django.db import models

class ServerProvider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='server_providers/logos/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Server Provider"
        verbose_name_plural = "Server Providers"
