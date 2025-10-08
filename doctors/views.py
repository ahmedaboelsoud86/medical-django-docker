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


@login_required(login_url='/login')
@permission_required("doctors.view_doctor",login_url='/login',raise_exception=True)
def index(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request,'doctors/index.html',context)


@login_required(login_url='/login')
@permission_required("doctors.add_doctor",login_url='/login',raise_exception=True)
def CreateDoctor(request):
    doctorForm = DoctorForm()
    userForm = UserForm()
    #Doctor.objects.all().delete()
    if request.method == 'POST':
        #photo = request.POST.get('photo')
        #return HttpResponse(photo)
        doctorForm = DoctorForm(request.POST, request.FILES)
        userForm = UserForm(request.POST)
        if  doctorForm.is_valid() and userForm.is_valid():
            #return HttpResponse("done")
            doctor = doctorForm.save(commit=False)
            selected_branche=request.POST.get('branche')
            password = request.POST.get('password')
            username = request.POST.get('username')
            phone = request.POST.get('phone')
            status = request.POST.get('status')
            email = request.POST.get('email')
            #return HttpResponse(selected_branches)
            branch = Branch.objects.get(pk=selected_branche)
            user = User.objects.create(email=email,status=status,username=username,branche=branch,phone=phone)
            user.set_password(password)
            user.save()
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
        