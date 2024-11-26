from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class user_register(models.Model):
    USER_ROLES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    username = models.CharField(max_length=100, unique=True)
    register = models.CharField(max_length=10, choices=USER_ROLES)
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=128)  # Password # 

    def __str__(self):
        return self.username

class city_table(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    stateISO = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    countryISO = models.CharField(max_length=100)

    def __str__(self):
        return self.city

class PatientDocument(models.Model):
    patient_name = models.CharField(max_length=100, default='Unknown Patient')  # Default value
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='patient_records/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient

class Prescription(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    prescription_details = models.TextField()
    medicines = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient_name} by {self.doctor_name}"

