from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import user_register
from django.http import JsonResponse
from .models import city_table
from .models import PatientDocument
from django.contrib import messages
from .models import Prescription  
from xhtml2pdf import pisa
from django.template.loader import get_template

# Create your views here.

def register1(request):
    return render(request,'Registration.html')

def login(request):           
    return render(request,'Login.html')

def homepage(request):          ## loading the home page  #
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Verify user exists and retrieve user information
        user = user_register.objects.filter(username=username, password1=password).first()
        if user:
            request.session['user_role'] = user.register  # Store 'patient' or 'doctor' in session 
        else:
            # Handle login error
            return render(request, 'Login.html', {'error': 'Invalid credentials'})
    return render(request,'HomePage.html')


def book_appoint(request):         # loading the book appointment page #
    return render(request,'BookAppointment.html')

def book_appoint2(request):
    return render(request,'BookAppointment.html')

def upload_record(request):    # loading the upload record page for patient #
    return render(request,'Uploadrecord.html')

def upload_document(request):  # func for uploading the patient document in the database #  
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')  # Get patient name from the form
        document_name = request.POST.get('document_name')  # Get document name from form (text input)
        document_file = request.FILES.get('record_file')  # Get the file from form (file input)
        request.session['patient_name'] = patient_name
        # Save document with patient name and document file
        if patient_name and document_file and document_name:
            # Create a new record in the database
            document_instance = PatientDocument(
                patient_name=patient_name,
                document_name=document_name,
                document_file=document_file
            )
            document_instance.save()
            messages.success(request, 'Document uploaded successfully.')

            print("Document uploaded successfully.")
           
        else:
            print("Error: Missing patient name or document.")
    
    return render(request, 'HomePage.html')
         
def get_cities(request, province):   # func of feetching cities in dropdown #
    cities = city_table.objects.filter(state=province).values_list('city', flat=True)
    cities_list = list(cities)  # Convert to a list of city names
    return JsonResponse(cities_list, safe=False)

def registerdb(request):     # function to save registration page values in the database #
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


def upload_record_redirect(request):    # function gets called when the user clicks upload record on home page #
    # Assuming user role is saved in the session or retrieved via the model
    user_role = request.session.get('user_role')  # Or retrieve from the user model

    # Redirect based on user role
    if user_role == 'patient':
        return redirect('upload_record')  # Redirects to Uploadrecord.html
    elif user_role == 'doctor':
        return redirect('patient_list')  # Redirects to Patientlist.html
    else:
        
        return redirect('homepage')

def upload_prescription_redirect(request):    # function gets called when the user clicks Generate prescription on home page #
    user_role = request.session.get('user_role')  

    # Redirect based on user role
    if user_role == 'patient':
        return redirect('view_prescriptions')  # Redirects to Uploadrecord.html
    elif user_role == 'doctor':
        return redirect('prescription_list')  # Redirects to Patientlist.html
    else:
        # Handle any cases where the role is not recognized
        return redirect('homepage')

def patient_list(request):    #when doctor is logged in he can see list of patients who have uploaded docs#
    # Fetch unique patient names with uploaded documents
    patients = PatientDocument.objects.values('patient_name').distinct()
    return render(request, 'Patientlist.html', {'patients': patients})

def prescription_list(request):
    patients = PatientDocument.objects.values('patient_name').distinct()
    return render(request, 'Prescriptionlist.html', {'patients': patients})

def view_documents(request, patient_name):        
    documents = PatientDocument.objects.filter(patient_name=patient_name)
    context = {
        'patient_name': patient_name,
        'documents': documents
    }
    return render(request, 'Documentlist.html', context)


def generate_prescription(request,patient_name):   #function to generate prescription by the doctor# 
    if request.method == 'POST':
      
        doctor_name = request.session.get('user_role')  # Assuming doctor name is in session
        prescription_details = request.POST.get('prescription_details')
        medicines = request.POST.get('medicines')
        
        if prescription_details and medicines:
            # Save prescription to the database
            prescription = Prescription(
                patient_name=patient_name,
                doctor_name=doctor_name,
                prescription_details=prescription_details,
                medicines=medicines,
            )
            prescription.save()
            messages.success(request, 'Prescription generated successfully!')
            return redirect('prescription_list')  # Redirect back to patient list        
        else:
            messages.error(request, 'All fields are required!')

    # Render the form to generate a prescription
    context = {'patient_name': patient_name}
    return render(request, 'GeneratePrescription.html', context)

def view_prescriptions(request):  #when user is logged in as patient hee can view his prescriptions written by the doctor# 
    
    patient_name = request.session.get('patient_name')  # fetching from the upload records page #
    print(f"Patient Name (session): '{patient_name}'")
    if not patient_name:
        messages.error(request, 'No patient with this name')  
   
    patient_name = str(patient_name).strip()
    prescriptions = Prescription.objects.filter(patient_name__iexact=patient_name)
  
    print(f"Prescriptions QuerySet: {prescriptions}")
    print(f"Raw SQL: {prescriptions.query}")
    return render(request, 'View_prescription.html', {'prescriptions': prescriptions})

   
def download_prescription_pdf(request, prescription_id):   # function to download and view the prescription in pdf form
    prescription = get_object_or_404(Prescription, id=prescription_id)

   
    patient_name = request.session.get('patient_name')
    if prescription.patient_name != patient_name:
        return HttpResponse('Unauthorized', status=401)

    # Load prescription template and generate PDF
    template = get_template('prescription_pdf.html')
    context = {'prescription': prescription}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prescription_{prescription.id}.pdf"'

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response 
    
   
