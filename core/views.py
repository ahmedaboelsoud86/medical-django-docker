from django.shortcuts import render, redirect 
from .models import Post, Category
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms  import PostForm,GroupForm
from django.http import HttpResponse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType 
import json  
def index(request):
    posts = Post.objects.all()
    if 1 == 1:
        messages.success(request, _('Form submitted successfully!'), extra_tags="alert alert-success")
    else:
        messages.warning(request, _('Please correct the errors below.'), extra_tags="alert alert-danger")
    context = {'posts':posts}
    return render(request,'core/index.html',context)

def CreatePost(request):
    form = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # cat_id = request.POST.get('category')
            # category_instance = Category.objects.get(id=cat_id) # Get the Category object with ID 1
            # p = Post()
            # p.set_current_language('en')
            # p.title = request.POST.get('title_en')
            # p.content = request.POST.get('content_en')
            # p.set_current_language('ar')
            # p.title = request.POST.get('title_ar')
            # p.content = request.POST.get('content_ar')
            # p.category = category_instance
            # p.save()
            form.save()
            messages.success(request,'Add Successfully')
            return redirect('/')
    context = {'form':form}
    return render(request,'core/form.html',context)

def deletepost(request,pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/')
    return redirect('/')

def updatepost(request,pk):
    post = Post.objects.get(id=pk)
   # return HttpResponse(post)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('/')

    context = {'form':form,'pk':pk}
    return render(request,'core/form.html',context)

def permission(request):
    mod, created = Group.objects.get_or_create(name="9999")
    permissions_list = Permission.objects.all()
    mod.permissions.set(permissions_list)
   # ct = ContentType.objects.get_for_model(model=Post)
    #perms = Permission.objects.filter(content_type=ct)
    
    #mod.permissions.add(*perms)
    #mod.permissions.add(24,25)
    
    permissions = Permission.objects.all()
    context = {'permissions':permissions}
    return render(request,'core/test.html',context)

def groups(request):
    groups = Group.objects.all()
    context = {'groups':groups}
    return render(request,'core/groups.html',context)

def createGroup(request):
    form = GroupForm
    permissions = Permission.objects.all()
    # groups = Group.objects.all()
    # for group in groups:
    #      group_permissions = group.permissions.all()
    # group_ids = Group.objects.all().values_list('id', flat=True)  
    # group_permissions = Permission.objects.filter(group__id__in=group_ids)
    # return HttpResponse(group_permissions)
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            mod = form.save()
            ids =  request.POST.getlist('permissions')
            #return HttpResponse(ids)
            mod.permissions.add(*ids)   
            messages.success(request,'Add Successfully')
            return redirect('/core/users/groups')
    context = {'form':form,'permissions':permissions}
    return render(request,'core/group_form.html',context)

def deletegroup(request,pk):
    group = Group.objects.get(id=pk)
    if request.method == 'POST':
        group.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/core/users/groups')
    return redirect('/users/groups')

def updateGroup(request,pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)
    group_permissions = group.permissions.all().values_list('id', flat=True)
    permissions = Permission.objects.all()

    #return HttpResponse(group_permissions)
    if request.method == 'POST':
        form = GroupForm(request.POST,instance=group)
        if form.is_valid():
            form.save()
            ids =  request.POST.getlist('permissions')
            group.permissions.clear()
            group.permissions.add(*ids)
            messages.success(request,'Updated Successfully')
            return redirect('/core/users/groups')

    context = {'permissions':permissions,'form':form,'pk':pk,'group_permissions':group_permissions}
    return render(request,'core/group_form.html',context)

# def permissions(request):
#     permissions = Permission.objects.all()
#     context = {'permissions': permissions}
#     return render(request,'core/permissions.html',context)





    

   