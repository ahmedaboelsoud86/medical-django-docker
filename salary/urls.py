from django.urls import path 
from . import views

app_name = 'salary'

urlpatterns = [
   path('bonuses', views.bonuses,name='bonuses'),
   path('create/bonuse', views.createBonuse,name='create-bonuse'),
]