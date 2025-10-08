from django.shortcuts import render
from patients.models import Patient,Profit
from patients.serializers  import PatientSerializer
from doctors.models import Doctor
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import HttpResponse
from datetime import date
from django.db.models.functions import ExtractMonth
import calendar




@login_required(login_url='/login')
# @permission_required("branches.add_branch",login_url='/login',raise_exception=True)
def index(request):

  profits = Profit.objects.annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        total_price=Sum('price')
    ).order_by('month')
  
  results_with_names = []
  for entry in profits:
    month_number = entry['month']
    month = calendar.month_name[month_number]
    results_with_names.append({
        'month': month,
        'total_price': entry['total_price']
    })
  month = []
  price = []
  for val in results_with_names:
      month.append(val['month'])
      price.append(int(val['total_price']))
  #month, total_price = zip(*results_with_names)
  #month = list(month)
  #total_price = list(total_price)
     
  #print(test)
  context = {'results_with_names':results_with_names,'month':month,'price':price}
  return render(request,'dashboard/index.html',context)

def topCounter(request):
  today = date.today()
  current_year = today.year
  current_month = today.month
  
  patient = Patient.objects.count()
  doctor = Doctor.objects.count()
  month_profits = Profit.objects.filter(created_at__year=current_year,created_at__month=current_month).aggregate(total=Sum('price'))['total']
  year_profits = Profit.objects.filter(created_at__year=current_year).aggregate(total=Sum('price'))['total']
  return JsonResponse({'data': {
     'patients_count':patient,
     'doctors_count':doctor,
     'month_profits':month_profits,
     'year_profits':year_profits,
  }})



def getProfits(request):
  profits = Profit.objects.annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        total_price=Sum('price')
    ).order_by('month')
  
  results_with_names = []
  for entry in profits:
    month_number = entry['month']
    month = calendar.month_name[month_number]
    results_with_names.append({
        'month': month,
        'total_price': entry['total_price']
    })
  month = []
  price = []
  for val in results_with_names:
      month.append(val['month'])
      price.append(int(val['total_price']))

  data = {
        'month': month,
        'price': price,
    }
  return JsonResponse(data) 
# $profits = Profit::whereYear('created_at', $request->datepicker)->select(
#                             DB::raw("(sum(price)) as price"),
#                             DB::raw("(DATE_FORMAT(created_at, '%b')) as month"))
#                             ->orderBy('created_at')
#                             ->groupBy(DB::raw("DATE_FORMAT(created_at, '%b')"))->get(); 

# [
#   {
#     "price": "333444",
#     "month": "Sep"
#   }
# ]
