from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

import base64
import hashlib

class SshPublicKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ssh_keys')
    name = models.CharField(max_length=10)
    key = models.TextField()
    fingerprint = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def clean(self):
        if not self.key:
            raise ValidationError({"key": "SSH public key cannot be empty."})
        
        parts = self.key.strip().split()
        if len(parts) < 2:
            raise ValidationError({"key": "Invalid SSH public key format."})
        key_body = parts[1]

        try:
            decoded_key = base64.b64decode(key_body.encode('utf-8'))
        except (base64.binascii.Error, ValueError):
            raise ValidationError({"key": "Invalid base64 encoding in SSH public key."})
        
        fingerprint = hashlib.sha256(decoded_key).hexdigest()

        qs = SshPublicKey.objects.filter(fingerprint=fingerprint)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({"key": "This SSH public key is already in use."})
        
        self.fingerprint = fingerprint
        return super().clean()
    
    def save(self, *args, **kwargs):
        if not self.fingerprint:
            self.full_clean()
        super().save(*args, **kwargs)