from django.db import models
from django.conf import settings

class Organization(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='organizations')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

class GitHubOrganization(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='github_orgs')
    github_org_id = models.PositiveIntegerField(unique=True)
    login = models.CharField(max_length=255)
    installation_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.login
    
    class Meta:
        verbose_name = "GitHub Organization"
        verbose_name_plural = "GitHub Organizations"