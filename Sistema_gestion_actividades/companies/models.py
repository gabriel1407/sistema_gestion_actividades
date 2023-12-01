import datetime

import logging
import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth import get_user_model
from jsonfield import JSONField
#from users.models import UserCustomer
# Create your models here.

User = get_user_model()

class Company(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    is_enabled = models.BooleanField(default=True)
    #users = models.ManyToManyField(User)
    #users = models.ManyToManyField('users.UserCustomer')
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'comp_companies_t'
        app_label = 'companies'


class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=180, null=False, blank=False)
    is_enabled = models.BooleanField(default=True)
    user = models.ManyToManyField('users.UserCustomer', blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'comp_departments_t'
        app_label = 'companies'


class Roles(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'comp_roles_t'
        app_label = 'companies'
