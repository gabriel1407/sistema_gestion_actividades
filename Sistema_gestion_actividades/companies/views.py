import datetime

import requests

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
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
from companies.serializers import UserSerializer

# Create your views here.

# def login_view(request):

#        if request.method == 'POST':
#             username = User.objects.get(username='gabriel.carvajal')
#             password = User.objects.get(password=request.data.get('password'))
#             user = authenticate(request, username=username, password=password)

#             print('username', username)
#             print('password', password)
#             print('user', user)

#             if user:
#                 login(request, user)
#                 return Response('Usuario ingresado', status=status.HTTP_200_OK)
#             else:
#                 return Response('Usuario no encontrado', status=status.HTTP_400_BAD_REQUEST)

#         return Response('Usuario ingresado', status=status.HTTP_200_OK)


"""class LoginViewSet(GenericAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    @csrf_exempt
    def post(self, request, format=None):
        try:
            
            username = self.request.POST['username']
            password = self.request.POST['password']
            user = authenticate(request, username=username, password=password)

            print('user', user)
            print(request)

            if user is not None:
                login(request, user)
                #return Response('Usuario ingresado', status=status.HTTP_200_OK)
            return Response('Usuario ingresado', status=status.HTTP_200_OK)
        except Exception as e:
            return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)"""


def signin(request):
    if request.method == 'POST':
        return Response('Usuario ingresado', status=status.HTTP_200_OK)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return Response('Usuario no existe', status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return redirect('tasks')
