from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .models import Pharmacy
from .forms import  PharmacyForm 
from  django.contrib  import messages 
import json  
from django.contrib.auth.decorators import login_required, permission_required 


# @login_required(login_url='/login')
# @permission_required("branches.view_branch",login_url='/login',raise_exception=True)
def index(request):
    pharmacies = Pharmacy.objects.all()
    context = {'pharmacies': pharmacies}
    return render(request,'pharmacies/index.html',context)

def createPharmacy(request):
    form = PharmacyForm
    if request.method == 'POST':
        form = PharmacyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Add Successfully')
            return redirect('/pharmacies')

    context = {'form':form}
    return render(request,'pharmacies/pharmacy_form.html',context)

def deletePharmacy(request,pk):
    pharmacy = Pharmacy.objects.get(id=pk)
    if request.method == 'POST':
        pharmacy.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/pharmacies')
    return redirect('/pharmacies')

def updatePharmacy(request,pk):
    pharmacy = Pharmacy.objects.get(id=pk)
    form = PharmacyForm(instance=pharmacy)
    if request.method == 'POST':
        form = PharmacyForm(request.POST,instance=pharmacy)
        if form.is_valid():
            #return HttpResponse(pk)
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('/pharmacies')

    context = {'form':form,'pk':pk}
    return render(request,'pharmacies/pharmacy_form.html',context)


