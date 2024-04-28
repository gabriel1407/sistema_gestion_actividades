from django.conf import settings
from rest_framework import serializers
from clinic.models import Clinic, Email, PhoneNumber

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('number', 'extension')
        read_only_fields = ("id", "created")
        
        
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('address',)
        read_only_fields = ("id", "created")
        
        
class ClinicListSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Clinic
        fields = ('__all__')
        read_only_fields = ("id", "created")
        
        
