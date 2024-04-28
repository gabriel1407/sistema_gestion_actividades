from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from companies.models import Company, Department, Roles
from users.models import UserCustomer, PatientsCustomers
from surgery.models import Surgery
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


class PatientsCustomersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientsCustomers
        fields = ('__all__')
        read_only_fields = ('email', 'username',)


class PatientsCustomersSerializer(serializers.ModelSerializer):
    #companies = CompanySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')
        read_only_fields = ('email', 'username',)

class SurgerySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserCustomer.objects.all(), many=True, required=False)
    patients = serializers.PrimaryKeyRelatedField(queryset=PatientsCustomers.objects.all(), many=True, required=False)
    class Meta:
        model = Surgery
        fields = ('__all__')
        read_only_fields = ('email', 'username',)


class SurgeryListSerializer(serializers.ModelSerializer):
    # AGREGA EL SERIALIZER DE TU MODELS CLINIC AQUI
    user = UserCustomerDetailSerializer(many=True, read_only=True)
    patients = PatientsCustomersDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Surgery
        fields = ('__all__')
        read_only_fields = ('email', 'username',)



