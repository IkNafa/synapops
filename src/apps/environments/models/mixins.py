from django.db import models
from django.core.exceptions import ValidationError

class EnvironmentMixin(models.Model):
    REQUIRED_ENVIRONMENT_TYPE = None
    
    environment = models.OneToOneField(to='environments.Environment', on_delete=models.CASCADE, related_name='%(class)s')

    class Meta:
        abstract = True

    def clean(self):
        super().clean()

        try:
            environment = self.environment
        except Exception:
            return

        if self.REQUIRED_ENVIRONMENT_TYPE is None:
            return

        if self.environment.type != self.REQUIRED_ENVIRONMENT_TYPE:
            raise ValidationError(
                f"{self.__class__.__name__} requiere "
                f"environment.type='{self.REQUIRED_ENVIRONMENT_TYPE}'"
            )

    def save(self, *args, **kwargs):
        if self.REQUIRED_ENVIRONMENT_TYPE:
            self.environment.type = self.REQUIRED_ENVIRONMENT_TYPE
            self.environment.save(update_fields=['type'])
        return super().save(*args, **kwargs)

        