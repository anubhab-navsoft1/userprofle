from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length = 255, db_index = True, null = False)
    address = models.CharField(max_length = 255, db_index = True, null = False)
    city = models.CharField(max_length = 255, db_index = True, null = False)
    state = models.CharField(max_length = 255, db_index = True, null = False)
    conutry = models.CharField(max_length = 255, db_index = True, null = False)

    def __str__(self):
        return self.user.username 