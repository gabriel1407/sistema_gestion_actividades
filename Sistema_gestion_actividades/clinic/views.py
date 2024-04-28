from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from clinic.models import PhoneNumber
from clinic.serializers import PhoneNumbersSerializer

class PhoneNumberViewSet(ModelViewSet):
    serializer_class = PhoneNumbersSerializer
    queryset = PhoneNumber.objects.all()
    filter_backends = (DjangoFilterBackend,)

