from django.db import models
from django.contrib.auth.models import AbstractUser


GENDERS = ['Male', 'Female']


class User(AbstractUser):
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=max([len(x) for x in GENDERS]), choices=zip(GENDERS, GENDERS))
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    REQUIRED_FIELDS = ['email', 'date_of_birth', 'gender', 'city', 'country']
