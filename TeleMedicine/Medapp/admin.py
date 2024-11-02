from django.contrib import admin
from .models import user_register  # Import your model

@admin.register(user_register)  # Register your model
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'register', 'email','password1')  # Customize what fields to display in the admin list view
