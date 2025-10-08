from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import  SalaryForm, UserForm,RegisterForm, salaryAttributeForm
from salary.models import Bonus, salaryattribute
from  django.contrib  import messages
import json  
from .models import User
from branches.models import Branch
from django.contrib.auth.models import Group, Permission
#from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets, status
from django.contrib.auth.decorators import login_required, permission_required 
from salary.models import Salary


# @login_required(login_url='/login')
# @permission_required("branches.view_branch",login_url='/login',raise_exception=True)
def index(request):
    users = User.objects.exclude(doctor__isnull=False)
    context = {'users': users}
    return render(request,'users/index.html',context)

def CreateUser(request):
    userForm = UserForm()
    salaryForm = SalaryForm()
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        salaryForm = SalaryForm(request.POST)
        if  userForm.is_valid() and salaryForm.is_valid():
            selected_branche=request.POST.get('branche')
            password = request.POST.get('password')
            username = request.POST.get('username')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            #return HttpResponse(selected_branches)
            branch = Branch.objects.get(pk=selected_branche)
            user = User.objects.create(email=email,username=username,branche=branch,phone=phone)
            user.set_password(password)
            user.save()
            price = request.POST.get('price')
            Salary.objects.create(user_id=user.id,price=price)
            messages.success(request,'Added Successfully')
            return redirect('/users')        
    context = {'userForm':userForm,'salaryForm':salaryForm}
    return render(request,'users/user_form.html',context)


def updateUser(request,pk):
    user = User.objects.get(id=pk)
    userForm = UserForm(instance=user)
    salaryForm = SalaryForm(instance=user.salary)
    if request.method == 'POST':
        
        userForm =  UserForm(request.POST,instance=user)
        salaryForm =  SalaryForm(request.POST,instance=user.salary)
        if  userForm.is_valid() and salaryForm.is_valid():
            userForm.save()
            #return HttpResponse("sadasd")
            salaryForm.save()
            messages.success(request,'Updated Successfully')
            return redirect('/users')
    context = {'userForm':userForm,'salaryForm':salaryForm, 'pk':pk}
    return render(request,'users/user_form.html',context)



def deleteUser(request,pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/users')
    return redirect('/users')

def deleteAllUser(request):
    if request.method == 'POST':
        ids =  request.POST.getlist('record_ids')
        # return HttpResponse(ids)
        a = json.loads(ids[0])
        lent = len(a)
        users = User.objects.filter(pk__in=a)
        users.delete() 
        #print(f"Type View  : {type(fromhtml[0])}")
        messages.success(request,f"{lent} users Deleted Successful  !!!")
        return redirect('/users') 
        
def userPermissions(request,pk):
    user = User.objects.get(pk=pk)
    groups = Group.objects.all()
    permissions = Permission.objects.all()


    user_permissions = list(user.user_permissions.all().values_list('id', flat=True))

    #
   # group_ids_flat = user.groups.values_list('id', flat=True)
    group_ids = list(user.groups.all().values_list('id', flat=True))
    #print(group_ids_flat)
    if request.method == 'POST':
        groups_ids =  request.POST.getlist('groups')
        permissions_ids =  request.POST.getlist('permissions')
        user.groups.set(groups_ids)
        user.user_permissions.set(permissions_ids)
        messages.success(request,'Successfully')
        return redirect('/users')
    context = {'groups':groups,'permissions':permissions,'pk':pk,'user_permissions':user_permissions,'group_ids':group_ids}
    return render(request,'users/user_permissions_form.html',context)

 
def clearUserGroup(request,pk):
    user = User.objects.get(pk=pk)
    user.groups.clear()
    messages.success(request,'Cleared Successfully')
    return redirect('/users/user_permissions/'+str(pk))


def clearUserPermissions(request,pk):
    user = User.objects.get(pk=pk)
    user.user_permissions.clear()
    messages.success(request,'Cleared Successfully')
    return redirect('/users/user_permissions/'+str(pk))
      

def signUp(request):
    if request.method == "POST":
        form  = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/en') 
    else:
        form  = RegisterForm(request.POST)
    return render(request,'registration/sign_up.html',{'form':form})


def employees(request):
    #users = User.objects.all()
    users = User.objects.filter(doctor__isnull=True)
    context = {'users': users}
    return render(request,'users/employees.html',context)


def monthlySalaries(request,pk):
    user = User.objects.get(pk=pk)
    
    new_date = user.created_at + timedelta(days=365)
    monthlysalary = 0
    if hasattr(user,'salary'):
        monthlysalary = user.salary.price
    bonuses = Bonus.objects.filter(created_at__gt=new_date).order_by('created_at')
    for item in bonuses:
       # print(monthlysalary)
        monthlysalary += monthlysalary * item.amount / 100
    
    per_day = monthlysalary / 30    
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    increase = user.salaryttributes.all().filter(status=1,created_at__year=current_year,created_at__month=current_month)
    deduction = user.salaryttributes.all().filter(status=0,created_at__year=current_year,created_at__month=current_month)
    
    
    increase_sum =  increase.aggregate(amount=Sum('amount'))
    deduction_sum =  deduction.aggregate(amount=Sum('amount'))
    
    if increase_sum['amount'] is None: 
        increase_sum['amount'] = 0
        
    if deduction_sum['amount'] is None: 
        deduction_sum['amount'] = 0    
    #net_salary =  + monthlysalary  + increase_sum['amount'] * per_day  - deduction_sum['amount'] * per_day
    net_dayes = increase_sum['amount']  - deduction_sum['amount']
    net_salary =   monthlysalary  +  net_dayes * per_day
    #print(increase_sum['amount'])
    context = {'net_salary':net_salary,'increase_sum':increase_sum,'deduction_sum':deduction_sum,'user': user,'monthlysalary':monthlysalary,'increase':increase,'deduction':deduction}
    return render(request,'users/salaries.html',context)


def deductionsIncentives(request):
    users = User.objects.filter(doctor__isnull=True)
    context = {'users': users}
    return render(request,'users/deductions_incentives.html',context)



def addDeductionsIncentives(request):
    form = salaryAttributeForm
    if request.method == 'POST':
        form = salaryAttributeForm(request.POST)
        if form.is_valid():
            #salaryattribute.objects.create(status=status,reason=reason,amount=amount,user_id=user_id) 
            instance = form.save(commit=False)
            instance.status = request.POST.get('status')
            form.save()
            messages.success(request,'Add Successfully')
            return redirect('/users/deductions_incentives')
    context = {'form':form}
    return render(request,'users/add_deductions_incentives.html',context)