from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from companies.models import Roles, Company
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class UserCustomer(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, null = True)
    email = models.EmailField(unique=True, null = True)
    first_name = models.CharField(max_length=200, null = True)
    last_name = models.CharField(max_length=200, null = True)
    is_active = models.BooleanField(default=False)
    rol = models.ForeignKey(Roles, related_name='rol', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)
    
    class Meta:
        db_table = 'users_models'
        app_label = 'users'
        
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True