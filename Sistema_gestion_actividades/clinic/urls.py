from django.urls import re_path
from rest_framework.routers import DefaultRouter
from clinic.views import PhoneNumberViewSet

router = DefaultRouter()
router.register(r'phone_numbers', PhoneNumberViewSet)

urlpatterns = []

urlpatterns += router.urls