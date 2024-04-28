from django.db import models
from django.utils import timezone


# Create your models here.
class BaseModel(models.Model):
    modified = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Clinic(BaseModel):
    name = models.CharField(max_length=150, null=False, blank=False)
    rif = models.CharField(max_length=10, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=True)
    
    class Meta:
        db_table = 'cl_clinic_t'
        app_label = "clinic"
        
        
class PhoneNumber(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=7, null=False)
    extension = models.CharField(max_length=4, null=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=True)
    
    class Meta:
        db_table = 'cl_clinic_phone_numbers_t'
        app_label = "clinic"


class Email(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='emails')
    address = models.EmailField(null=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=True)
    
    class Meta:
        db_table = 'cl_clinic_emails_t'
        app_label = "clinic"
    
    