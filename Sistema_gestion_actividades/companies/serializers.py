from django.conf import settings
from rest_framework import serializers
from companies.models import Company, Department
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    #companies = CompanySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')
        read_only_fields = ('email', 'username',)

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

class DepartmentListSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(many=False, read_only=True)
    class Meta:
        model = Department
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)