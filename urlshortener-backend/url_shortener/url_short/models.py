from django.db import models
import string, secrets
from datetime import timedelta
from django.utils import timezone

# Create your models here.

ALPHABET = string.ascii_letters + string.digits

class Link(models.Model):
    code = models.CharField(max_length=30,unique=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveBigIntegerField(default=0)
    expires = models.DateTimeField(null=True, blank=True)

    def save(self,*args, **kwargs):
        if not self.code:
            self.code = ''.join(secrets.choice(ALPHABET) for _ in range(7))
        super().save(*args, **kwargs)
    def is_expired(self):
        return self.expires and timezone.now() > self.expires