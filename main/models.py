from django.contrib.auth import get_user_model
from django.db import models

class UserRole(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(get_user_model(), related_name='role')
