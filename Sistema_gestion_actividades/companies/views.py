import datetime

import requests

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
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
from django.contrib.auth.models import User
from companies.serializers import UserSerializer, CompanySerializer, CompanyListSerializer, DepartmentListSerializer, DepartmentSerializer, UserListSerializer, \
    UserCreateSerializer, UserListSerializer, UserRoleSerializer, UserPasswordChangeSerializer, UserRoleListSerializer
from companies.models import Company, Department, Roles

# Create your views here.
User = get_user_model()

class LoginViewSet(GenericAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        try:
            user = User.objects.filter(username=str(request.data.get('username')))
            
            
            if user is not None:
                return Response({'access': (True), 'data': UserListSerializer(instance=user, many=True).data}, status=status.HTTP_200_OK)
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
    


class UserViewSet(APIView):
    #permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer
    filter_backends = (DjangoFilterBackend)
    
    def get(self, request, *args, **kwargs):
        my_data = get_user_model().objects.all()
        serializer = UserListSerializer(my_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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

        
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data.get('password'))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        my_data = get_user_model().objects.get(pk=pk)
        serializer = UserListSerializer(my_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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

        user_serializer = UserListSerializer(instance=instance, data=request.data, partial=True)
        
        if user_serializer.is_valid(raise_exception=True):
            #user_serializer.validated_data['password'] = make_password(user_serializer.validated_data.get('password'))
            user_serializer.save()
            return Response(UserListSerializer(instance=user_serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.kwargs.get('pk')
        user.save()
        return Response({'User deleted', user.username}, status=status.HTTP_200_OK)
 


class ChangePasswordViewSet(APIView):
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserPasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            user.password = make_password(serializer.validated_data.get('password'))
            user.save(update_fields=['password'])
            return Response({'message': 'Password changed', "User": user}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordViewSet(APIView):
    def put(self, request, pk):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserPasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            user.password = make_password(serializer.validated_data.get('password'))
            user.save(update_fields=['password'])
            return Response({'message': 'Password changed', "User": user.username}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    
class UserRolViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsCompanyPermission)
    serializer_class = UserRoleListSerializer
    queryset = Roles.objects.all()
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    filter_fields = ('company_id',)
    
    def create(self, request, *args, **kwargs):
        serializer = UserRoleSerializer(Roles(), data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(UserRoleListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        modulo_instance = self.get_object()

        serializer = UserRoleListSerializer(instance=modulo_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(UserRoleListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)