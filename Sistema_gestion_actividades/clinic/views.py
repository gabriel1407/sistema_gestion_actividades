from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from clinic.models import Clinic
from clinic.serializers import ClinicListSerializer, PhoneNumberSerializer, EmailSerializer 

class ClinicViewSet(ModelViewSet):
    serializer_class = ClinicListSerializer
    queryset = Clinic.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'name', 'created',)

    def create(self, request, *args, **kwargs):
        clinic_data = request.data
        phone_numbers_data = clinic_data.pop('phone_numbers', [])
        emails_data = clinic_data.pop('emails', [])

        serializer = self.get_serializer(data=clinic_data)
        serializer.is_valid(raise_exception=True)
        clinic = serializer.save()

        self._create_related_objects(clinic, phone_numbers_data, emails_data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        clinic = self.get_object()
        clinic_data = request.data
        phone_numbers_data = clinic_data.pop('phone_numbers', [])
        emails_data = clinic_data.pop('emails', [])

        serializer = self.get_serializer(clinic, data=clinic_data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_clinic = serializer.save()

        self._update_related_objects(updated_clinic, phone_numbers_data, emails_data)

        return Response(serializer.data)

    def _create_related_objects(self, clinic, phone_numbers_data, emails_data):
        for phone_number_data in phone_numbers_data:
            phone_number_data['clinic'] = clinic.id
            phone_number_serializer = PhoneNumberSerializer(data=phone_number_data)
            phone_number_serializer.is_valid(raise_exception=True)
            phone_number_serializer.save()

        for email_data in emails_data:
            email_data['clinic'] = clinic.id
            email_serializer = EmailSerializer(data=email_data)
            email_serializer.is_valid(raise_exception=True)
            email_serializer.save()

    def _update_related_objects(self, clinic, phone_numbers_data, emails_data):
        clinic.phone_numbers.all().delete()
        clinic.emails.all().delete()

        self._create_related_objects(clinic, phone_numbers_data, emails_data)