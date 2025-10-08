from django.urls import path # type: ignore
from . import views

app_name = 'branches'

urlpatterns = [
   path('', views.index,name='index'),
   path('create', views.CreateBranch,name='create'),
   path('update/<int:pk>/', views.updatebranch,name='update'),
   path('delete/<int:pk>/', views.deletebranch,name='delete'),
   path('delete/all', views.deleteAllbranch,name='deleteall'),


]