from django.http.response import JsonResponse 
from django.shortcuts import render, redirect 
from .models import Patient,Appointment,Expense,Ray
from  tools.models import Tool
from .forms import PatientForm,AppointmentForm, ExpenseForm
from branches.models import Branch
from patients.serializers import PatientSerializer, AppointmentSerializer, ExpenseSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import query_patients_by_args,query_appointment_by_args, query_expense_by_args
from rest_framework.exceptions import MethodNotAllowed
from django.http import HttpResponse
from  django.contrib  import messages 
from django.contrib.auth.decorators import login_required, permission_required
import json  
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from datetime import date
from django.contrib.auth.decorators import login_required, permission_required 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
 

@login_required(login_url='/login')
@permission_required("patients.view_patient",login_url='/login',raise_exception=True)
def index(request):
    #return JsonResponse("pppp")
    branches = Branch.objects.all()
    context = {'branches': branches}
    return render(request,'patients/index.html',context)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


    # def create(self, request, *args, **kwargs):
    #     #return Response("hhhhhhhhhhhhhh")
    #     return Response(request.POST.get("title"))
    #     raise MethodNotAllowed(method='POST', detail='Creation of new instances is not allowed.')
    
    # def update(self, request, *args, **kwargs):
    #         raise MethodNotAllowed('PUT')

    # def partial_update(self, request, *args, **kwargs):
    #         raise MethodNotAllowed('PATCH')
    
    # def destroy(self, request, *args, **kwargs):
    #     raise MethodNotAllowed(method='DELETE', detail='deleteing is not allowed.')
    

    def list(self, request, **kwargs):
        try:
            print(request.query_params)
            music = query_patients_by_args(**request.query_params)
            #return Response(music)
            serializer = PatientSerializer(music['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = music['draw']
            result['recordsTotal'] = music['total']
            result['recordsFiltered'] = music['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        #except Exception as e:
         #   return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
        

   

# def patients_data(request):
#    if  request.is_ajax():
#        time = time()
#        data = Patient.objects.all()
#        list_data = []
       

def list_patients(request):
    patients = Patient.objects.all()
    if request.method == 'POST' and request.is_ajax():
        gender = request.POST.get('gender')
        print("555555555555555555555")
      #  patients = Patient.objects.filter(gender=gender)\
    print("pppppppppppppppppppppp999999999999999999999999")  
    data = [patient.to_dict_json() for  patient in patients]
    response = {'data':data,'draw':0,'recordsTotal':patients.count(),'recordsFiltered':1}
    return JsonResponse(response)

def CreatePatient(request):
    #return HttpResponse("dasdasd")
    patientForm = PatientForm()
    context = {'patientForm':patientForm}
    return render(request,'patients/patient_form.html',context)
#     userForm = UserForm()
#     #Doctor.objects.all().delete()
#     if request.method == 'POST':
#         #photo = request.POST.get('photo')
#         #return HttpResponse(photo)
#         doctorForm = DoctorForm(request.POST, request.FILES)
#         userForm = UserForm(request.POST)
#         if  doctorForm.is_valid() and userForm.is_valid():
#             doctor = doctorForm.save(commit=False)
#             selected_branche=request.POST.get('branche')
#             password = request.POST.get('password')
#             username = request.POST.get('username')
#             phone = request.POST.get('phone')
#             status = request.POST.get('status')
#             email = request.POST.get('email')
#             #return HttpResponse(selected_branches)
#             branch = Branch.objects.get(pk=selected_branche)
#             user = User.objects.create(email=email,status=status,username=username,branche=branch,phone=phone)
#             user.set_password(password)
#             user.save()
#             doctor.user = user
#             doctor.save()
#             messages.success(request,'Added Successfully')
#             return redirect('/doctors')        
#     context = {'doctorForm':doctorForm,'userForm':userForm}
#     return render(request,'doctors/doctor_form.html',context)


def updatePatient(request,pk):
    pass    
#     doctor = Doctor.objects.get(user_id=pk)
#     user = doctor.user
#     userForm = UserForm(instance=user)
#     doctorForm = DoctorForm(instance=doctor)
#     if request.method == 'POST':
#         userForm =  UserForm(request.POST, request.FILES,instance=user)
#         doctorForm =  DoctorForm(request.POST, request.FILES,instance=doctor)
#         if  userForm.is_valid() and doctorForm.is_valid():
#             userForm.save()
#             doctorForm.save()
#             messages.success(request,'Updated Successfully')
#             return redirect('/doctors')

#     context = {'userForm':userForm,'doctorForm':doctorForm, 'pk':pk}
#     return render(request,'doctors/doctor_form.html',context)



def deletePatient(request,pk):
    pass
#     doctor = Doctor.objects.get(id=pk)
#    # return HttpResponse(doctor)
#     if request.method == 'POST':
#         doctor.delete() 
#         messages.success(request,'Deleted Successfully')
#         return redirect('/doctors')
#     return redirect('/doctors')

def deleteAllPatient(request):
    #return HttpResponse("asdas")
    if request.method == 'POST':
        ids =  request.POST.getlist('record_ids')
        a = json.loads(ids[0])
        lent = len(a)
        patients = Patient.objects.filter(pk__in=a)
        patients.delete() 
        #print(f"Type View  : {type(fromhtml[0])}")
        messages.success(request,f"{lent} Patients Deleted Successful  !!!")
        return redirect('/patients') 
        
@login_required(login_url='/login')
def patientAppointment(request,pk):
    patient = Patient.objects.get(pk=pk)
    appointments = Appointment.objects.filter(patient_id=pk)
    context = {'appointments':appointments,'patient':patient,'pk':pk}
    return render(request,'patients/patientAppointment.html',context)


@login_required(login_url='/login')
def createAppointment(request,pk):
    appointmentForm = AppointmentForm()
    if request.method == 'POST':
        appointmentForm = AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointmentForm.save(commit=False)
            appointmentForm.patient = request.POST.get('patient')
            appointmentForm.save()
            messages.success(request,'Add Successfully')
            return redirect('/patients/appointments/'+str(pk))
    context = {'pk':pk,'appointmentForm': appointmentForm}
    return render(request,'patients/add_appointment.html',context)



@api_view(['GET'])
@login_required(login_url='/login')
def doctorsAppointmentData(request):
    doctor = request.GET.get('doctor', '')
    appdata = request.GET.get('appdata', '')
    
    #my_models = Appointment.objects.filter(doctor_id=doctor).filter(appdata=appdata)
    #my_models = Appointment.objects.filter(Q(doctor_id=doctor) | Q(appdata=appdata))
    #my_models = Appointment.objects.filter(Q(doctor_id=doctor))
    #my_models = Appointment.objects.filter(Q(appdata=appdata))            
    my_models = query_appointment_by_args(**request.query_params)

    print(my_models)        
    serializer = AppointmentSerializer(my_models['items'], many=True)
    return Response(serializer.data)
    # $appointment = Appointment::where('user_id',$q->doctor)
    #                               ->where('appdata',$q->appdata)
    #                               ->with('patients')->get();
    # return response()->json(['data' => $appointment]);


@login_required(login_url='/login')
def updateAppointment(request,pk):
    pass

@login_required(login_url='/login')
def deleteAppointment(request,pk):
    appointment = Appointment.objects.get(id=pk)
    if request.method == 'POST':
        appointment.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/patients/appointments/'+str(appointment.patient_id))
    return redirect('/patients/appointments/'+str(appointment.patient_id))



@login_required(login_url='/login')
def patientProfile(request,pk):
    patient = Patient.objects.get(pk=pk)
    appointments = patient.appointments.all()
    pharmacies = patient.expenses.all()
    context = {'patient':patient,'appointments':appointments,'pharmacies':pharmacies}
    return render(request,'patients/profile.html',context)




def medicationsPatients(request):
    tools = Tool.objects.all()
    patients = Patient.objects.all()
    context = {'tools': tools,'patients':patients}
    return render(request,'patients/medications_patients.html',context)



class MedicationsViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer  
   
    def list(self, request, **kwargs):
        try:
            music = query_expense_by_args(**request.query_params)
            #return Response(music)
            serializer = ExpenseSerializer(music['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = music['draw']
            result['recordsTotal'] = music['total']
            result['recordsFiltered'] = music['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        #except Exception as e:
         #   return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

def addMedicationsToPatient(request):
    expenseForm = ExpenseForm()
    if request.method == 'POST':
        expenseForm = ExpenseForm(request.POST)
        if expenseForm.is_valid():
            expenseForm.save()
            messages.success(request,'Add Successfully')
            return redirect('patients:medications')
    context = {'expenseForm': expenseForm}
    return render(request,'patients/add_medications_patient.html',context)



def deleteMedications(request):
    if request.method == 'POST':
        row = request.POST.get('row')
        expense = Expense.objects.get(id=row)
        expense.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('patients:medications')
    return redirect('patients:medications')


def updateMedications(request,pk):
    expense = Expense.objects.get(pk=pk)
    expenseForm = ExpenseForm(instance=expense)
    if request.method == 'POST':
        expenseForm =  ExpenseForm(request.POST, instance=expense)
        if  expenseForm.is_valid():
            expenseForm.save()
            messages.success(request,'Updated Successfully')
            return redirect('patients:medications')
    context = {'expenseForm': expenseForm}
    return render(request,'patients/add_medications_patient.html',context)
        
  
  
  
@login_required(login_url='/login')
def patientInvoice(request,pk):
    #patient = Patient.objects.get(pk=pk)
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.all()
    pharmacies = patient.expenses.all()
    total_appointments = 0
    for item in appointments :
        if item.profits.all():
            total_appointments += item.profits.first().price
    
    total_pharmacies = 0
    for item in pharmacies :
        total_pharmacies += item.tool.price * item.amount     
    context = {'total_pharmacies':total_pharmacies,'patient':patient,'appointments':appointments,'pharmacies':pharmacies,'total_appointments':total_appointments}
    return render(request,'patients/invoice.html',context)


@csrf_exempt
def uploadRayes(request,pk):
    mv_dict = request.FILES
    print(mv_dict['images[]'])
    #image_file = request.FILES['image']
    my_image = Ray.objects.create(patient_id=pk,photo=mv_dict['images[]'])     
    return HttpResponse()

@csrf_exempt
def deleteRay(request,pk):
    print(pk)
    ray = Ray.objects.get(pk=pk)
    ray.delete()
    #mv_dict = request.FILES
    #print(mv_dict['images[]'])
    #image_file = request.FILES['image']
    #my_image = Ray.objects.create(patient_id=pk,photo=mv_dict['images[]'])     
    return HttpResponse(pk)        
        
        
        
