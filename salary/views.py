from django.shortcuts import render, redirect 
from rest_framework import viewsets, status
from .models import salaryattribute
from .forms import  BonusForm
from  django.contrib  import messages 
from rest_framework.response import Response
from .models import Bonus, query_deductionsIncentives_by_args
from salary.serializers import deductionsIncentivesSerializer
from django.contrib.auth.decorators import login_required, permission_required 
from django.http import HttpResponse

# @login_required(login_url='/login')
# @permission_required("branches.view_branch",login_url='/login',raise_exception=True)
class deductionsIncentivesViewSet(viewsets.ModelViewSet):
    queryset = salaryattribute.objects.all()
    serializer_class = deductionsIncentivesSerializer

    def list(self, request, **kwargs):
        try:
            print(request.query_params)
            music = query_deductionsIncentives_by_args(**request.query_params)
            #return Response(music)
            serializer = deductionsIncentivesSerializer(music['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = music['draw']
            result['recordsTotal'] = music['total']
            result['recordsFiltered'] = music['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        #except Exception as e:
         #   return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
        


def bonuses(request):
    bonus = Bonus.objects.all()
    context = {'bonus': bonus}
    return render(request,'salary/bonuses.html',context)


def createBonuse(request):
    form = BonusForm()
    if request.method == 'POST':
        form = BonusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Add Successfully')
            return redirect('/salary/bonuses')
    context = {'form':form}
    return render(request,'salary/bonus_form.html',context)


class BookViewSet(viewsets.ModelViewSet):
    queryset = salaryattribute.objects.all()
    serializer_class = deductionsIncentivesSerializer

    # def list(self, request):
    #     return HttpResponse("list")

    # def create(self, request):
    #     return HttpResponse("create")

    # def retrieve(self, request, pk=None):
    #     return HttpResponse(pk)

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     return HttpResponse("destroy")

# class TestViewSet(viewsets.ModelViewSet):
#     queryset = salaryattribute.objects.all()
#     serializer_class = deductionsIncentivesSerializer 
    
#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         serializer_class.is_valid()
#         return HttpResponse("create")
    
#     def list(self, request, **kwargs):
#          return HttpResponse("list")