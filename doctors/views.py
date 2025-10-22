from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .models import Doctor
from .forms import  DoctorForm , UserForm
from  django.contrib  import messages 
import json  
from users.models import User
from branches.models import Branch
from django.shortcuts import get_object_or_404
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required 
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class DoctorListView(LoginRequiredMixin,ListView):
    model = Doctor
    
    # @method_decorator(login_required)
    # def dispatch(self,  *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    # filter
    # def get_queryset(self):
    #     queryset = super(DoctorListView,self).get_queryset()
    #     queryset = queryset.filter(user = self.request.user)
    #     return queryset
    #context_object_name = ''
    #template_name=''
    


# @login_required(login_url='/login')
# @permission_required("doctors.view_doctor",login_url='/login',raise_exception=True)
# def index(request):
#     doctors = Doctor.objects.all()
#     context = {'doctors': doctors}
#     return render(request,'doctors/index.html',context)


@login_required(login_url='/login')
@permission_required("doctors.add_doctor",login_url='/login',raise_exception=True)
def CreateDoctor(request):
    doctorForm = DoctorForm()
    userForm = UserForm()
    if request.method == 'POST':
        doctorForm = DoctorForm(request.POST, request.FILES)
        userForm = UserForm(request.POST)
        if  doctorForm.is_valid() and userForm.is_valid():
            user = userForm.save(commit=False)
            password = request.POST['password']
            user.set_password(password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.success(request,'Added Successfully')
            return redirect('/doctors')        
    context = {'doctorForm':doctorForm,'userForm':userForm}
    return render(request,'doctors/doctor_form.html',context)

@login_required(login_url='/login')
@permission_required("doctors.change_doctor",login_url='/login',raise_exception=True)
def updateDoctor(request,pk):
    doctor = get_object_or_404(Doctor, user_id=pk)
    user = doctor.user
    userForm = UserForm(instance=user)
    doctorForm = DoctorForm(instance=doctor)
    if request.method == 'POST':
        userForm =  UserForm(request.POST, request.FILES,instance=user)
        doctorForm =  DoctorForm(request.POST, request.FILES,instance=doctor)
        if  userForm.is_valid() and doctorForm.is_valid():
            userForm.save()
            doctor.brief = request.POST.get('brief')
            doctor.birthday = request.POST.get('birthday')
            doctor.save(update_fields=['brief', 'birthday'])
            #doctorForm.save()
            messages.success(request,'Updated Successfully')
            return redirect('/doctors')
    context = {'userForm':userForm,'doctorForm':doctorForm, 'pk':pk}
    return render(request,'doctors/doctor_form.html',context)


@login_required(login_url='/login')
@permission_required("doctors.delete_doctor",login_url='/login',raise_exception=True)
def deleteDoctor(request,pk):
    doctor = Doctor.objects.get(id=pk)
   # return HttpResponse(doctor)
    if request.method == 'POST':
        doctor.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/doctors')
    return redirect('/doctors')


@login_required(login_url='/login')
@permission_required("doctors.can_deleteall_doctors",login_url='/login',raise_exception=True)
def deleteAllDoctor(request):
    if request.method == 'POST':
        ids =  request.POST.getlist('record_ids')
        a = json.loads(ids[0])
        lent = len(a)
        doctors = Doctor.objects.filter(pk__in=a)
        doctors.delete() 
        #print(f"Type View  : {type(fromhtml[0])}")
        messages.success(request,f"{lent} doctors Deleted Successful  !!!")
        return redirect('/doctors') 
        