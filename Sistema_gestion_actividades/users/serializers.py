from django.conf import settings
from rest_framework import serializers
from task.models import Task, TaskHistory
from companies.models import Company, Department
from companies.serializers import DepartmentListSerializer, UserListSerializer
from users.models import UserCustomer

class UserCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserCustomer
        fields = ('__all__')

class UserCustomerListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserCustomer
        fields = ('__all__')
