from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .models import Branch
from .forms import  BranchForm 
from  django.contrib  import messages 
import json
from django.contrib.auth.decorators import login_required, permission_required  


@login_required(login_url='/login')
@permission_required("branches.view_branch",login_url='/login',raise_exception=True)
def index(request):
    branches = Branch.objects.all()
    context = {'branches': branches}
    return render(request,'branches/index.html',context)


@login_required(login_url='/login')
@permission_required("branches.add_branch",login_url='/login',raise_exception=True)
def CreateBranch(request):
    form = BranchForm
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Add Successfully')
            return redirect('/branches')

    context = {'form':form}
    return render(request,'branches/branch_form.html',context)

@login_required(login_url='/login')
@permission_required("branches.delete_branch",login_url='/login',raise_exception=True)
def deletebranch(request,pk):
    branch = Branch.objects.get(id=pk)
    if request.method == 'POST':
        branch.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/branches')
    return redirect('/branches')


@login_required(login_url='/login')
@permission_required("branches.change_branch",login_url='/login',raise_exception=True)
def updatebranch(request,pk):
    branch = Branch.objects.get(id=pk)
    form = BranchForm(instance=branch)
    if request.method == 'POST':
        form = BranchForm(request.POST,instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('/branches')

    context = {'form':form,'pk':pk}
    return render(request,'branches/branch_form.html',context)


@login_required(login_url='/login')
@permission_required("branches.can_deleteall_branches",login_url='/login',raise_exception=True)
def deleteAllbranch(request):
    if request.method == 'POST':
        ids =  request.POST.getlist('record_ids')
        a = json.loads(ids[0])
        lent = len(a)
        branchs = Branch.objects.filter(pk__in=a)
        branchs.delete() 
        #print(f"Type View  : {type(fromhtml[0])}")
        messages.success(request,f"{lent} branches Deleted Successful  !!!")
        return redirect('/branches') 
        
