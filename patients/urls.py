from django.urls import path 
from . import views

app_name = 'patients'

urlpatterns = [
   path('', views.index, name='index'),
   path('list_patients/', views.list_patients, name='list_patients'),
   path('create_patient', views.CreatePatient, name='create'),
   path('update_patient/<int:pk>/', views.updatePatient, name='update_patient'),
   path('delete_patient/<int:pk>/', views.deletePatient, name='delete_patient'),
   path('delete_all_patient', views.deleteAllPatient, name='deleteallpatient'),
   path('profile/<int:pk>/', views.patientProfile, name='patient_profile'),
   path('invoice/<int:pk>/', views.patientInvoice, name='patient_invoice'),

   path('appointments/<int:pk>/', views.patientAppointment,name='appointments'),
   
   path('create_appointment/<int:pk>/', views.createAppointment,name='create_appointment'),
   path('update/appointment/<int:pk>/', views.updateAppointment,name='update_appointment'),
   path('delete/appointment/<int:pk>/', views.deleteAppointment,name='delete_appointment'),
   path('appointment/data/', views.doctorsAppointmentData,name='appointment_data'),
   
   path('medications/', views.medicationsPatients,name='medications'),
   path('add/medications/patient/', views.addMedicationsToPatient,name='add_medications'),

   path('delete/medications/', views.deleteMedications,name='delete_medications'),

   path('update/medications/<int:pk>/', views.updateMedications,name='update_medications'),
   
   path('upload_rayes/<int:pk>/', views.uploadRayes,name='upload_rayes'),
   path('delete_raye/<int:pk>/', views.deleteRay,name='delete_ray'),
   
   

   


   

   
]
