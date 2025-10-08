from django.urls import path # type: ignore
from . import views

#from rest_framework.routers import DefaultRouter
#router = DefaultRouter()


urlpatterns = [
   path('', views.index,name='dashboard'),
   path('top', views.topCounter,name='top-counter'),
   #path('get-profits', views.getProfits,name='get-profits'),
   path('get/profits/page', views.getProfitsPage,name='get-profits-page'),
]