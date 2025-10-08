from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .models import Tool
from .forms import  ToolForm 
from  django.contrib  import messages 
import json  
from django.contrib.auth.decorators import login_required, permission_required  

# @login_required(login_url='/login')
# @permission_required("branches.view_branch",login_url='/login',raise_exception=True)
def index(request):
    tools = Tool.objects.all()
    context = {'tools': tools}
    return render(request,'tools/index.html',context)

def createTool(request):
    form = ToolForm
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Add Successfully')
            return redirect('/tools')

    context = {'form':form}
    return render(request,'tools/tool_form.html',context)

def deleteTool(request,pk):
    tool = Tool.objects.get(id=pk)
    if request.method == 'POST':
        tool.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/tools')
    return redirect('/tools')

def updateTool(request,pk):
    tool = Tool.objects.get(id=pk)
    form = ToolForm(instance=tool)
    if request.method == 'POST':
        form = ToolForm(request.POST,instance=tool)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('/tools')

    context = {'form':form,'pk':pk}
    return render(request,'tools/tool_form.html',context)


