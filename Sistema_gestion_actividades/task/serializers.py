from django.conf import settings
from rest_framework import serializers
from task.models import Task, TaskHistory, project_tasks
from companies.models import Company, Department
from companies.serializers import DepartmentListSerializer, UserListSerializer, CompanyListSerializer, UserCustomerDetailSerializer
from django.contrib.auth.models import User

class project_tasks_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = project_tasks
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

class project_tasks_list_serializer(serializers.ModelSerializer):
    owner = UserCustomerDetailSerializer(many=False, read_only=True)
    departament = DepartmentListSerializer(many=False, read_only=True)
    class Meta:
        model = project_tasks
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)
        
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

class TaskListSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(many=False, read_only=True)
    project = project_tasks_list_serializer(many=False, read_only=True)
    user = UserCustomerDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)
        
    """def get_user(self, obj):
       user = obj.user.all()
       return UserListSerializer(user, many=True).data"""

class TaskHistoryListSerializer(serializers.ModelSerializer):
    #company = DepartmentListSerializer(many=False, read_only=True)
    user = UserCustomerDetailSerializer(many=True, read_only=True)
    class Meta:
        model = TaskHistory
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

