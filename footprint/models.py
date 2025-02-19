from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils.timezone import now


# Create your models here.
class UserCarbonFootprint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    json_data = models.JSONField(null=False, blank=False)
    created_at = models.DateTimeField(default=now)

    class Meta:
        ordering = [F("created_at").desc(nulls_last=True)]
