from django.conf import settings
from rest_framework import serializers
from task.models import Task, TaskHistory, ChatsTasks
from companies.models import Company, Department
from companies.serializers import DepartmentListSerializer, UserListSerializer
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

class TaskListSerializer(serializers.ModelSerializer):
    company = DepartmentListSerializer(many=False, read_only=True)
    #user = UserListSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)
        
    """def get_user(self, obj):
       user = obj.user.all()
       return UserListSerializer(user, many=True).data"""

class TaskHistoryListSerializer(serializers.ModelSerializer):
    #company = DepartmentListSerializer(many=False, read_only=True)
    user = UserListSerializer(many=True, read_only=True)
    class Meta:
        model = TaskHistory
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)


class GetChatsTaskSerializer(serializers.ModelSerializer):
    user = UserListSerializer(many=True, read_only=True)
    class Meta:
        model = ChatsTasks
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)
