from django.urls import path 
from . import views


urlpatterns = [
   path('', views.listMessages,name='messages'),
   path('new_messages', views.newMessages,name='new_messages'),   
   path('message/<int:pk>/', views.detilsMessage,name='message'),
   path('deletemessage/<int:pk>/', views.deleteMessage,name='deletemessage'),
   path('delete_room/<int:pk>/', views.deleteRoom,name='delete_room'),

   
]