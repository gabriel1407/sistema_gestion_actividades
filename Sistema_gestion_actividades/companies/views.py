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
    


class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer
    filter_backends = (DjangoFilterBackend)
    ordering_fields = ('username', 'email')
    filter_fields = ('username', 'email')

    @action(methods=['get'], detail=True, )
    def check_username(self, request, pk=None):

        username = request.GET.get('username', None)
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesExits:
            return Response({}, status=status.HTTP_200_OK)

        return Response({'message': 'Username exists'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, )
    def check_email(self, request, pk=None):

        email = request.GET.get('email', None)
        UserModel = get_user_model()

        try:
            user_email = UserModel.objects.get(email=email)
        except UserModel.DoesExits:
            return Response({}, status=status.HTTP_200_OK)

        return Response({'message': 'Email exists'}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True)
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = UserPasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            user.password = make_password(serializer.validated_data.get('password'))
            user.save(update_fields=['password'])
            return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


    @action(methods=['post'], detail=True)
    def add_company(self, request, pk=None):

        user = self.get_object()

        serializer = UserCompanySerializer(data=request.data)

        if serializer.is_valid():
            if settings.APP_STAFF_CIA_VALIDATION and not user.is_superuser and not user.is_staff and user.companies.all().count() > 0:
                return Response({'error': {'message': 'This user is added to a company', 'code': 9800}},
                                status=status.HTTP_417_EXPECTATION_FAILED)

            company_id = serializer.data.get('company')
            company = Company.objects.get(id=company_id)
            user.companies.add(company)
            return Response({'message': 'Company added'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def remover_company(self, request, pk=None):

        user = self.get_object()

        serializer = UserCompanySerializer(data=request.data)

        if serializer.is_valid():
            company_id = serializer.data.get('company')

            if user.companies.filter(id=company_id).exists():
                company = Company.objects.get(id=company_id)
                user.companies.remove(company)
                return Response({'message': 'Company removed'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User is not associated with that company.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


    def create(self, request, *args, **kwargs):
        
        user_serializer = UserCreateSerializer(User(), data=request.data)
        # Validate data user information
        if user_serializer.is_valid():
            user_serializer.validated_data['password'] = make_password(user_serializer.validated_data.get('password'))
            user_serializer.save()
            #return Response(UserDetailsSerializer(instance=user_serializer.instance).data,status=status.HTTP_201_CREATED)
            return Response(UserListSerializer(instance=user_serializer.instance).data, status=status.HTTP_200_OK)
        else:
            #return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        user_serializer = UserUpdateSerializer(
            instance=instance, data=request.data, partial=True)
        
        if user_serializer.is_valid(raise_exception=True):
            #user_serializer.validated_data['password'] = make_password(user_serializer.validated_data.get('password'))
            user_serializer.save()
            return Response(UserDetailsSerializer(instance=user_serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.kwargs.get('pk')
        user.save()
        return Response({'User deleted', user.username}, status=status.HTTP_200_OK)
    
class UserRolViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsCompanyPermission)
    serializer_class = UserRoleSerializer
    queryset = Roles.objects.all()
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    filter_fields = ('company_id',)
    
    def create(self, request, *args, **kwargs):
        serializer = UserRoleSerializer(Roles(), data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(UserRoleSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        modulo_instance = self.get_object()

        serializer = UserRoleSerializer(instance=modulo_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(UserRoleSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)