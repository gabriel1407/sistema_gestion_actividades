import datetime

import logging
import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from jsonfield import JSONField
from companies.models import Department
# Create your models here.
class project_tasks(models.Model):
    name = models.CharField(max_length=180, null=False, blank=False)
    departament = models.ForeignKey(Department, null=False, on_delete=models.PROTECT)
    owner = models.ForeignKey('users.UserCustomer', null=False, on_delete=models.PROTECT)
    is_enabled = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'tasks_projects_t'
        app_label = 'task'
    

class Task(models.Model):
    name = models.TextField(blank=True, null=False)
    description = models.TextField(blank=True, null=True)
    is_enabled = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    porcentage_task = models.PositiveIntegerField(default=0) 
    user = models.ManyToManyField('users.UserCustomer')
    departament = models.ForeignKey('companies.Department', null=False, on_delete=models.PROTECT)
    project = models.ForeignKey(project_tasks, null=True, on_delete=models.PROTECT)
    start_day = models.DateField(null=False, blank=False)
    end_day = models.DateField(null=False, blank=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'tasks_task_t'
        app_label = 'task'

class TaskHistory(models.Model):
    name = models.TextField(blank=True, null=False)
    task = models.ForeignKey(Task, null=True, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    is_enabled = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    porcentage_task = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField('users.UserCustomer', null = False, blank=True)
    departament = models.ForeignKey('companies.Department', null=False, on_delete=models.PROTECT)
    project = models.ForeignKey(project_tasks, null=True, on_delete=models.PROTECT)
    start_day = models.DateField(null=False, blank=False)
    end_day = models.DateField(null=False, blank=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'tasks_task_history_t'
        app_label = 'task'
        

# class ChatsTasks(models.Model):
#     company = models.ForeignKey('companies.Department', null=False, on_delete=models.PROTECT)
#     user = models.ForeignKey('users.UserCustomer', null=False, blank=True, on_delete=models.PROTECT)
#     task = models.ForeignKey(Task, null=False,  blank=True, on_delete=models.PROTECT)
#     name = models.TextField(null = False)
#     is_enabled = models.BooleanField(default=True)
#     is_closed = models.BooleanField(default=False)
#     text = models.TextField(blank=True, null=True)
#     file = models.FileField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)
#     images = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)
#     last_activity = models.DateTimeField(default=timezone.now)
#     last_closed = models.DateField(null=False, blank=False)
#     created = models.DateTimeField(default=timezone.now, editable=False)
#     modified = models.DateTimeField(default=timezone.now, editable=False)

#     class Meta:
#         db_table = 'tasks_chats'
#         app_label = 'task'
