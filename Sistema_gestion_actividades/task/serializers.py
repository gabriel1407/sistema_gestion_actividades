from django.conf import settings
from rest_framework import serializers
from task.models import Task
from companies.models import Company, Department
from companies.serializers import DepartmentListSerializer
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

class TaskListSerializer(serializers.ModelSerializer):
    company = DepartmentListSerializer(many=False, read_only=True)
    class Meta:
        model = Task
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)