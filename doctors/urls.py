from django.urls import path 
from . import views

app_name = 'doctors'

urlpatterns = [
   path('', views.index,name='index'),
   path('create', views.CreateDoctor,name='create'),
   path('update/<int:pk>/', views.updateDoctor,name='update'),
   path('delete/<int:pk>/', views.deleteDoctor,name='delete'),
   path('delete/all', views.deleteAllDoctor,name='deleteall'),
]