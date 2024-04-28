from django.conf import settings
from rest_framework import serializers
from clinic.models import Clinic, PhoneNumber, Email

class PhoneNumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fiels = ('__a;;__')
        read_only_fields = ("id", "created")
        
