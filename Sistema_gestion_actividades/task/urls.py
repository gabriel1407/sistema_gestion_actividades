from django.urls import re_path
from rest_framework.routers import DefaultRouter


from task.views import TaskViewSet, ReportTaskFinished

router = DefaultRouter()
router.register(r'task', TaskViewSet)
router.register(r'report_task_finished', ReportTaskFinished)

urlpatterns = [
    #re_path(r'^login/$', LoginViewSet, name='login'),
    #re_path(r'^login/', LoginViewSet.as_view(), name='login'),

]

urlpatterns += router.urls