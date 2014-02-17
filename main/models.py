from django.contrib.auth import get_user_model
from django.db import models

class UserRole(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(get_user_model(), related_name='role')


class BrewtoadAccount(models.Model):
    brewtoad_user_id = models.PositiveIntegerField(unique=True, blank=False, null=False,
                                                   help_text='Your brewtoad user id')
    user = models.OneToOneField(get_user_model(), related_name='brewtoad_account')

    @property
    def url(self):
        return "http://brewtoad.com/users/%d" % self.brewtoad_user_id

