from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from companies.models import Company, Department, Roles
from users.models import UserCustomer
#from users.serializers import UserCustomerListSerializer
#from django.contrib.auth.models import User

User = get_user_model()

class UserCustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustomer
        fields = ('__all__')
        read_only_fields = ('email', 'username',)


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
    user = serializers.PrimaryKeyRelatedField(queryset=UserCustomer.objects.all(), many=True, required=False)
    class Meta:
        model = Department
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

class DepartmentListSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(many=False, read_only=True)
    user = UserCustomerDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'modified',)

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ('__all__')

class UserRoleListSerializer(serializers.ModelSerializer):
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
    
class UserUpdateSerializer(serializers.ModelSerializer):
    #rol_asignado = RolesUserSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('__all__')
        #read_only_fields = ('id', 'username')
        
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserCustomer
        fields = ('__all__')
        #ields = ('__all__')

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user