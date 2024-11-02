from django.urls import path
from . import views 

urlpatterns=[
path('Registration/', views.register1, name='register'),
path('Registration/Login/', views.login, name='login'),
path('register/', views.registerdb, name='register'),
path('HomePage/', views.homepage, name='homepage'),
path('BookAppointment/', views.book_appoint, name='book_appoint'),
path('BookAppointment/get-cities/<str:province>', views.book_appoint2, name='book_appoint2'),
path('BookAppointment/get-cities/<str:province>', views.get_cities, name='get_cities'),
]