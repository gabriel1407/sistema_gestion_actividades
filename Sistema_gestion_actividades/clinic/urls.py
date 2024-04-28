from django.urls import re_path
from rest_framework.routers import DefaultRouter
from clinic.views import ClinicViewSet

router = DefaultRouter()
router.register(r'clinic', ClinicViewSet)

urlpatterns = []

urlpatterns += router.urls