import datetime

import requests

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.utils.timezone import localtime
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.utils import timezone
from rest_framework import status, serializers
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action, api_view
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from companies.serializers import UserSerializer, CompanySerializer, CompanyListSerializer, DepartmentListSerializer, DepartmentSerializer
from companies.models import Company, Department

# Create your views here.


class LoginViewSet(GenericAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        try:
            user = User.objects.filter(username=str(request.data.get('username')), password = request.data.get('password'))
            
            
            if user is not None:
                return Response({'access': (True), 'data': UserSerializer(instance=user, many=True).data}, status=status.HTTP_200_OK)
            #return Response({ 'messages': (False)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'messages': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsSuperUser)
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_enabled',)


    def create(self, request, *args, **kwargs):
        serialize = CompanySerializer(data=request.data)

        if serialize.is_valid():
            serialize.save()
            return Response(CompanyListSerializer(instance=serialize.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        company = self.get_object()
        serialize = CompanySerializer(company, data=request.data, partial=True)

        if serialize.is_valid():
            serialize.save()

            return Response(CompanyListSerializer(instance=serialize.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class DepartmentViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsCompanyPermission)
    serializer_class = DepartmentListSerializer
    queryset = Department.objects.all()
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    filter_fields = ('company_id', 'is_enabled',)
    search_fields = ('name',)

    def create(self, request, *args, **kwargs):
        serializer = DepartmentSerializer(Department(), data=request.data)

        if serializer.is_valid():
            serializer.save()
            #audit.set_obj(serializer.instance)
            #audit.process()
            return Response(DepartmentListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        department_instance = self.get_object()
        serializer = DepartmentSerializer(instance=department_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            #audit.process()
            return Response(DepartmentListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        departamento = self.kwargs.get('pk')
        departamento.save()
        return Response({'departamento deleted', departamento}, status=status.HTTP_200_OK)
    

