from django.shortcuts import render,redirect
from  django.contrib  import messages 
from .forms import  messageForm
from .models import testmessage,Room
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count,Sum
from django.db.models.query import QuerySet
from collections import defaultdict
from django.contrib.auth import get_user_model
from django.db.models import Max, OuterRef, Subquery
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

def listMessages(request):
    user = request.user
    latest_messages_subquery = testmessage.objects.filter(
    room=OuterRef('room')
    ).order_by('-timestamp').values('pk')[:1]
    latest_messages = testmessage.objects.filter(
        pk=Subquery(latest_messages_subquery)
    ).filter(Q(sender=user) | Q(recipient=user)).select_related('room').order_by('-timestamp')
    context = {'latest_messages': latest_messages}
    return render(request,'inbox/index.html',context)




def deleteRoom(request,pk):
    room = Room.objects.filter(pk=pk)
    if request.method == 'POST':
        room.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('/')
    return redirect('/messages')



def detilsMessage(request,pk):
    messages_query = testmessage.objects.filter(room=pk)
    if len(messages_query) == 0:
        return redirect('/')
    user = request.user
    if user ==  messages_query[0].sender:
        recipient = messages_query[0].recipient
        #return HttpResponse(recipient)
    else:
        recipient = messages_query[0].sender
    form = messageForm()

    if request.method == 'POST':
         form = messageForm(request.POST)
         if form.is_valid():
            title = request.POST.get("title")
            content = request.POST.get("content")
            testmessage.objects.create(title=title,content=content,recipient=recipient,sender=user,room_id=pk)
            messages.success(request,'Sent Successfully')
            return redirect('/message/'+str(pk))
         
    context = {'messages_query': messages_query,'form':form,'recipient':recipient}
    return render(request,'inbox/detils_message.html',context)

def deleteMessage(request,pk):
    single_message = testmessage.objects.get(id=pk)
    room_id = single_message.room_id
    if request.method == 'POST':
        single_message.delete()
        room_with_counts = Room.objects.annotate(num_posts=Count('testmessages')).get(id=single_message.room_id)
        print(room_with_counts.num_posts)
        if room_with_counts.num_posts == 0:
           room_with_counts.delete()
        messages.success(request,'Deleted Successfully')
        return redirect('/message/'+str(room_id))
    return redirect('/message/'+str(room_id))


def newMessages(request):
    user = user=request.user
    form = messageForm(user=user)
    if request.method == 'POST':
        form = messageForm(request.POST,user=user)
        if form.is_valid():
            user = user=request.user
            other_user = request.POST.get("recipient")
            title = request.POST.get("title")
            content = request.POST.get("content")
            message = testmessage.objects.filter(Q(sender=user,recipient=other_user) | Q(sender=other_user,recipient=user)).first()
            #return HttpResponse(message)
            if message :
                room_id = message.room_id
            else:
                room_id = Room.objects.create().id
            testmessage.objects.create(title=title,content=content,recipient_id=other_user,sender=user,room_id=room_id)
            messages.success(request,'Sent Successfully')
            return redirect('/')
    context = {'form':form}
    return render(request,'inbox/create.html',context)
