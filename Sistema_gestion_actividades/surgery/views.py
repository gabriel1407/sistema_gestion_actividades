import datetime

import requests

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.utils.timezone import localtime
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status, serializers
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action, api_view
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from users.models import UserCustomer
from users.serializers import UserCustomerListSerializer
from django.contrib.auth.models import User
from surgery.models import Surgery
from surgery.serializers import SurgerySerializer, SurgeryListSerializer
# Create your views here.
User = get_user_model()

class SurgeryViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsCompanyPermission)
    serializer_class = SurgeryListSerializer
    queryset = Surgery.objects.all()
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    
    def create(self, request, *args, **kwargs):
        serializer = SurgerySerializer(Surgery(), data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(SurgeryListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        modulo_instance = self.get_object()

        serializer = SurgerySerializer(instance=modulo_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(SurgeryListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)