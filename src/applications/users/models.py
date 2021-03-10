from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F','Female'),
        ('O', 'Others')
    )

    username = models.CharField( max_length=12, unique=True)
    email = models.EmailField()
    name = models.CharField(max_length=20, blank=True)
    last_names = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    #
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.name + ' ' + self.last_names

    def __str__(self):
        return self.name + ' ' + self.last_names