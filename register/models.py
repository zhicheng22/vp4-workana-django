from django.db import models
from django.contrib.auth.models import User


class BaseUser(models.Model):
    user = models.OneToOneField(User, db_index=True, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=11)
    house_number = models.CharField(max_length=10)
    street_address = models.CharField(max_length=20)
    subdivision = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=4)
    logo_cover = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.user.username