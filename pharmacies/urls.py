from django.urls import path # type: ignore
from . import views

app_name = "pharmacies"

urlpatterns = [
   path('', views.index,name='index'),
   path('create/pharmacy', views.createPharmacy,name='create'),
   path('update/pharmacy/<int:pk>/', views.updatePharmacy,name='update'),
   path('delete/pharmacy/<int:pk>/', views.deletePharmacy,name='delete'),
]