from django.db import models
from register.models import BaseUser
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Type(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Complaint_Model(models.Model):

    INPROGRESS = 'IN PROGRESS'
    RESOLVED = 'RESOLVED'
    UNRESOLVED = 'UNRESOLVED'
    ADMIN_RESOLVE_CHOICES = [
        (INPROGRESS, 'IN PROGRESS'),
        (RESOLVED, 'RESOLVED'),
        (UNRESOLVED, 'UNRESOLVED'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    respondent_first_name = models.CharField(max_length=50)
    respondent_last_name = models.CharField(max_length=50)
    respondent_address = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=100)
    complain = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    resolution = models.CharField(max_length=100, blank=True, choices=ADMIN_RESOLVE_CHOICES)
    comments = models.CharField(max_length=100, blank=True)
    is_submitted = models.BooleanField(blank=True, default=False)
    is_canceled = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.subject

