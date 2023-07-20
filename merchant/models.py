from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from.managers import CustomMerchantManager
# Create your models here.

class MerchantUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomMerchantManager()