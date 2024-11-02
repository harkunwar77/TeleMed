from django.db import models
# Create your models here.
class user_register(models.Model):
    USER_ROLES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    username = models.CharField(max_length=100, unique=True)
    register = models.CharField(max_length=10, choices=USER_ROLES)
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=128)  # Password field 

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