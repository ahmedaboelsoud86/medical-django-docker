"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static 



from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
# from Patient import views
from patients.views import PatientViewSet, MedicationsViewSet,index
from salary.views import deductionsIncentivesViewSet,BookViewSet

router = DefaultRouter()

router.register(r'books', BookViewSet)
router.register(r'patient', PatientViewSet)
router.register(r'medications', MedicationsViewSet,basename='medications')
router.register(r'deductions_incentives', deductionsIncentivesViewSet,basename='deductions_incentives')





urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('branches/', include('branches.urls')),
    path('doctors/', include('doctors.urls')),
    path('patients/', include('patients.urls')),
    path('users/', include('users.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('core/', include('core.urls')),
    path('tools/', include('tools.urls')),
    path('salary/', include('salary.urls')),
    path('pharmacies/', include('pharmacies.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('inbox.urls')),
    path('', include('django.contrib.auth.urls')),
    re_path(r'^api/', include(router.urls)),
    #prefix_default_language=False
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#prefix_default_language = False