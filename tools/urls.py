from django.urls import path # type: ignore
from . import views

app_name = 'tools'

urlpatterns = [
   path('', views.index,name='index'),
   path('create/tool', views.createTool,name='create'),
   path('update/tool/<int:pk>/', views.updateTool,name='update'),
   path('delete/tool/<int:pk>/', views.deleteTool,name='delete'),
]