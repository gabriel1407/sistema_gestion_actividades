from django.conf import settings
from rest_framework import serializers
from companies.models import Company
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    #companies = CompanySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')
        read_only_fields = ('email', 'username',)
