
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    image = models.URLField()
    jersey = models.IntegerField(default=0, null=True)
    position = models.CharField(max_length=30, null=True)
    tags = models.JSONField(default=list, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email

