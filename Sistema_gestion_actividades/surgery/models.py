import datetime

import logging
import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth import get_user_model
from jsonfield import JSONField
from clinic.models import Clinic
from users.models import PatientsCustomers
# Create your models here.

User = get_user_model()


class Surgery(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT)
    name = models.CharField(max_length=180, null=False, blank=False)
    is_enabled = models.BooleanField(default=True)
    user = models.ManyToManyField('users.UserCustomer', blank=True)
    patient = models.ManyToManyField(PatientsCustomers, blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'sur_surgery_t'
        app_label = 'surgery'


