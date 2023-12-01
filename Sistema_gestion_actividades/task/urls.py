from django.urls import re_path
from rest_framework.routers import DefaultRouter


from task.views import TaskViewSet, ReportTaskFinished

router = DefaultRouter()
router.register(r'task', TaskViewSet)

urlpatterns = [
    #re_path(r'^task/<int:pk>/', TaskViewSet, name='login'),
    re_path(r'^report_tasks/', ReportTaskFinished.as_view(), name='report_tasks')

]

urlpatterns += router.urls