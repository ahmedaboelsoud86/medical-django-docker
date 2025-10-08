from django.shortcuts import render, redirect 
from .models import Post, Category
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms  import PostForm
from django.http import HttpResponse


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
            cat_id = request.POST.get('category')
            category_instance = Category.objects.get(id=cat_id) # Get the Category object with ID 1

            p = Post()

            p.set_current_language('en')
            p.title = request.POST.get('title_en')
            p.content = request.POST.get('content_en')



            p.set_current_language('ar')
            p.title = request.POST.get('title_ar')
            p.content = request.POST.get('content_ar')
            
            p.category = category_instance

            p.save()
           
    
            messages.success(request,'Add Successfully')
            return redirect('/')

    context = {'form':form}
    return render(request,'core/create.html',context)

def deletepost(request,pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/')
    return redirect('/')

def updatepost(request,pk):
    post = Post.objects.get(id=pk)
    return HttpResponse(post)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('/')

    context = {'form':form,'pk':pk}
    return render(request,'core/create.html',context)