import datetime

import logging
import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from jsonfield import JSONField

# Create your models here.
class Task(models.Model):
    name = models.TextField(blank=True, null=False)
    is_enabled = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    user = models.ManyToManyField(User)
    departament = models.ForeignKey('companies.Department', null=False, on_delete=models.PROTECT)
    start_day = models.DateField(null=False, blank=False)
    end_day = models.DateField(null=False, blank=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'tasks_task_t'
        app_label = 'task'

class TaskHistory(models.Model):
    name = models.TextField(blank=True, null=False)
    is_enabled = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)
    user = models.ManyToManyField(User)
    departament = models.ForeignKey('companies.Department', null=False, on_delete=models.PROTECT)
    start_day = models.DateField(null=False, blank=False)
    end_day = models.DateField(null=False, blank=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'tasks_task_history_t'
        app_label = 'task'