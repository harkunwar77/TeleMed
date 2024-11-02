from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import user_register
from django.http import JsonResponse
from .models import city_table

# Create your views here.

def register1(request):
    return render(request,'Registration.html')

def login(request):
    return render(request,'Login.html')

def homepage(request):
    return render(request,'HomePage.html')

def book_appoint(request):
    return render(request,'BookAppointment.html')

def book_appoint2(request):
    return render(request,'BookAppointment.html')

def get_cities(request, province):
    cities = city_table.objects.filter(state=province).values_list('city', flat=True)
    cities_list = list(cities)  # Convert to a list of city names
    return JsonResponse(cities_list, safe=False)

def registerdb(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        register = request.POST.get('role')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        try:
            new_user = user_register(username=username, register=register, email=email, password1=password1)
            new_user.save()
            print("Data saved successfully")
        except Exception as e:
            print(f"Error saving data: {e}")
          
        return render(request, 'Registration.html')
    return render(request, 'Registration.html')



