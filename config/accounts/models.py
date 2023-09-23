from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import datetime


class User(AbstractBaseUser, PermissionsMixin):
    # user data
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    # user status
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    premium_expire_date = models.DateTimeField(blank=True, null=True)

    favorites = models.ManyToManyField('book.Book', related_name='favorites', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return "%s - %s" % (self.phone_number, self.full_name, )

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_premium(self) -> bool:
        if not self.premium_expire_date:
            return False
        return self.premium_expire_date <= datetime.datetime.now()


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
