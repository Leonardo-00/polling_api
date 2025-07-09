from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Account(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False)
    favorite_categories = models.ManyToManyField('polls.Category', blank=True)