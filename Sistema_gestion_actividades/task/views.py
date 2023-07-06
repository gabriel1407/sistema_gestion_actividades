import datetime
from datetime import datetime

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
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from task.models import Task, TaskHistory
from task.serializers import TaskListSerializer, TaskSerializer, TaskHistoryListSerializer
from task.filters import CreatedBetweenFilter
from companies.serializers import UserListSerializer
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
    

    def send_email(self,request , id, user, *args, **kwargs):
        try:
            
                
            user = User.objects.filter(id__in = user).first()
            
            #user2 = User.objects.filter(id__in = user).order_by("-id").first()
            #user = UserListSerializer(User.objects.filter(id__in = user), many=True).data
            task_day = Task.objects.filter(id = id).first()
            
            if user is not None:
                image = Image.open('C:/Users/gabri/OneDrive/Documentos/Repositorios-github/sistema_gestion/Sistema_gestion_actividades/task/templates/actividades-de-trabajo-en-equipo.png')
                new_image = image.resize((300, 99))
                print("users: ", user.username)
                #print("users: ", user2.username)
                
                html_msg = loader.render_to_string('C:/Users/gabri/OneDrive/Documentos/Repositorios-github/sistema_gestion/Sistema_gestion_actividades/task/templates/sendemail.html',
                    {
                        "Usuario": " ".join(list(map(lambda x: x.capitalize(), user.username.split(" ")))),
                        #"Usuario2": " ".join(list(map(lambda x: x.capitalize(), user2.username.split(" ")))),
                        "tarea": str(task_day.description),
                        'fecha_inicio': str(task_day.start_day),
                        'fecha_entrega': str(task_day.end_day),
                    }
                )
                html_msg = html_msg.replace('%% my_image %%','{{ my_image }}')
                email = EmailSender(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT,username=settings.EMAIL_HOST_USER,password=settings.EMAIL_HOST_PASSWORD)
                email.send(sender=settings.EMAIL_HOST_USER,receivers=[user.email, user.email],subject="Tarea Asignada",html=html_msg, body_images={ "my_image": new_image})
                return Response({'access': (True), 'User': user.username}, status=status.HTTP_200_OK)
    
            else:
                return Response({'Error': "el campo user no puede estar nulo"}, status=status.HTTP_400_BAD_REQUEST)
                
                    
        except Exception as e:
            return Response({'messages': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        serialize = TaskSerializer(data=request.data)

        if serialize.is_valid():
            start_day = serialize.validated_data['start_day']
            end_day = serialize.validated_data['end_day']
            
            start_day_actual = datetime.date(datetime.now())
            print(start_day_actual)
            #replace_data = start_day_actual.replace(microsecond=0)
            if start_day <= start_day_actual:
                return Response({'Messages': 'No puedes crear una tarea con una fecha del dia de ayer'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif end_day <= start_day:
                return Response({'Messages': 'La fecha de entrega tiene que ser mayor o igual al dia que se asigno la fecha'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            serialize.save()
            task_t = TaskListSerializer(instance=serialize.instance).data
            #self.send_email(request)
            #return Response(TaskListSerializer(instance=serialize.instance).data, status=status.HTTP_201_CREATED)
            return self.send_email(request, task_t["id"], task_t["user"])
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            task_update = self.get_object()
            serializer = TaskListSerializer(task_update, data=request.data, partial=True)


            if serializer.is_valid():
                task_finish = serializer.validated_data.get('is_finished')
                if task_finish == True:
                    serializer.save()
                    
                    #user_t = TaskListSerializer(instance=serializer.instance, partial = True).data
                    taks_history = TaskHistory()
                    user_t = Task.objects.filter(user__id__in = request.data.get('user'))
                    print('user_t, ', user_t)
                    #user = serializer.validated_data.get('user')
                    #print("user", user_t[task_update.user])
                    taks_history.task = task_update
                    taks_history.name = task_update.name
                    taks_history.description = task_update.description
                    taks_history.is_finished = task_update.is_finished
                    taks_history.user = task_update.user.set(user_t)
                    taks_history.departament = task_update.departament
                    taks_history.start_day = task_update.start_day
                    taks_history.end_day = task_update.end_day
                    taks_history.save()
                    return Response(TaskListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
                    
                else:
                    serializer.save()
                    return Response(TaskListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'messages': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ReportTaskFinished(ReadOnlyModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistoryListSerializer
    filter_backends = (DjangoFilterBackend, CreatedBetweenFilter)
    filter_fields = ('is_enabled',)