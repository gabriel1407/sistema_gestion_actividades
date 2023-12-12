from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
#from companies.models import Roles
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password, email, first_name=None, last_name=None, ci=None, phone = None, is_active=False, rol=None):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")
        if not ci:
            raise ValueError("El usuario debe tener un una cedula de identidad")
        if not password:
            raise ValueError("El usuario debe tener una contraseña")
        if not email:
            raise ValueError("El usuario debe tener un email")
        if UserCustomer.objects.filter(email=email).exists():
            raise ValueError("El email ya está registrado")
        user = self.model(
            username=username,
            #email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            ci = ci,
            phone = phone,
            rol=rol
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email, first_name=None, last_name=None, ci = None, phone = None, rol=None):
        user = self.create_user(
            username=username,
            #password=password,
            #email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            ci=ci,
            phone=phone,
            rol=rol
        )
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserCustomer(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    ci = models.CharField(max_length=255, unique=True, null=True)
    phone = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    rol = models.ForeignKey('companies.Roles', related_name='rol',on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        db_table = 'users_models'
        app_label = 'users'

    objects = UserManager()
