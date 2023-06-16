import datetime

import requests

from PIL import Image
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.utils.timezone import localtime
from django_filters.rest_framework import DjangoFilterBackend
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
from task.models import Task, TaskHistory
from task.serializers import TaskListSerializer, TaskSerializer
from redmail import EmailSender
from django.template import loader
# Create your views here.

User = get_user_model()

class TaskViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsSuperUser)
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_enabled',)


    def send_email(self, *args, **kwargs):
        try:
            user = User.objects.get(id=1)
            task_day = Task.objects.filter(id = 2)
            if user is not None:
                image = Image.open('/Sistema_gestion_actividades/task/templates/actividades-de-trabajo-en-equipo.png')
                new_image = image.resize((300, 99))

                html_msg = loader.render_to_string(
                    '/Sistema_gestion_actividades/task/templates/sendemail.html',
                    {
                        "Usuario": " ".join(list(map(lambda x: x.capitalize(), user.fullname.split(" ")))),
                        'fecha de inicio': str(task_day.start_day),
                        'fecha de entrega': str(task_day.end_day),
                    }
                )
                html_msg = html_msg.replace('%% my_image %%','{{ my_image }}')
                email = EmailSender(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT,username=settings.EMAIL_HOST_USER,password=settings.EMAIL_HOST_PASSWORD)
                email.send(sender=settings.EMAIL_HOST_USER,receivers=[user.email],subject="Tarea Asignada",html=html_msg, body_images={ "my_image": new_image})
        except Exception as e:
            return None
    
    def create(self, request, *args, **kwargs):
        serialize = TaskSerializer(data=request.data)

        if serialize.is_valid():
            serialize.save()
            self.send_email()
            return Response(TaskListSerializer(instance=serialize.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        
        task_update = self.get_object()
        serializer = TaskListSerializer(task_update, data=request.data, partial=True)

        if serializer.is_valid():
            task_finish = serializer.validated_data.get('is_finished')
            if task_finish == True:
                serializer.save()
                taks_history = TaskHistory()
                taks_history.id = serializer.get_fields('id')
                taks_history.name = serializer.validated_data.get('name')
                taks_history.description = serializer.validated_data.get('description')
                taks_history.is_finished = serializer.validated_data.get('is_finished')
                #taks_history.user = serializer.validated_data.get('user')
                taks_history.departament_id = serializer['departament']
                taks_history.start_day = serializer.validated_data.get('start_day')
                taks_history.end_day = serializer.validated_data.get('end_day')
                taks_history.save()
                return Response(TaskListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
                
            else:
                serializer.save()
                return Response(TaskListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

