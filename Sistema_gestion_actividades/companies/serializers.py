from django.conf import settings
from rest_framework import serializers
from companies.models import Company, Department, Roles
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

class UserRoleSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(many=False, read_only=True)
    class Meta:
        model = Roles
        fields = ('__all__')

class UserListSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(many=False, read_only=True)
    rol = UserRoleSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')
        
class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=16, required=True)
    
class UserCompanySerializer(serializers.Serializer):
    company = serializers.IntegerField(required=True)

    def validate(self, attrs):

        if attrs['company'] is not None:
            company_id = attrs['company']
            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                raise serializers.ValidationError("Company specify not exists")
        else:
            raise serializers.ValidationError("Company not specify")

        return attrs