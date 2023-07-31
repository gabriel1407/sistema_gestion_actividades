from django.urls import re_path
from rest_framework.routers import DefaultRouter


from task.views import TaskViewSet, ReportTaskFinished, DashboardUserViewSet

router = DefaultRouter()
router.register(r'task', TaskViewSet)
router.register(r'report_task_finished', ReportTaskFinished)

urlpatterns = [
    #re_path(r'^task/<int:pk>/', TaskViewSet, name='login'),
    re_path(r'^dashboard_manager/', DashboardUserViewSet.as_view(), name='dashboard_manager'),

]

urlpatterns += router.urls