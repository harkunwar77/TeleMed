from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns=[
path('Registration/', views.register1, name='register'),
path('Registration/Login/', views.login, name='login'),
path('register/', views.registerdb, name='register'),
path('HomePage/', views.homepage, name='homepage'),
path('BookAppointment/', views.book_appoint, name='book_appoint'),
path('BookAppointment/get-cities/<str:province>', views.book_appoint2, name='book_appoint2'),
path('BookAppointment/get-cities/<str:province>', views.get_cities, name='get_cities'),
path('Uploadrecord/', views.upload_record, name='upload_record'),
path('Uploadrecords/', views.upload_document, name='upload_document'),
path('upload_record_redirect/', views.upload_record_redirect, name='upload_record_redirect'),
path('PatientList/', views.patient_list, name='patient_list'),
path('prescription_list/', views.prescription_list, name='prescription_list'),
path('PatientList/<str:patient_name>/documents/', views.view_documents, name='view_documents'),
path('upload_prescription_redirect/', views.upload_prescription_redirect, name='upload_prescription_redirect'),
path('PatientList/<str:patient_name>/generate-prescription/', views.generate_prescription, name='generate_prescription'),
path('my-prescriptions/', views.view_prescriptions, name='view_prescriptions'),
path('download-prescription/<int:prescription_id>/', views.download_prescription_pdf, name='download_prescription'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




