from django.db import models
from django.conf import settings
from model_utils import Choices
from datetime import datetime


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'id'),
    ('2', 'id'),
    ('3', 'id'),
    ('4', 'id'),
)


class Salary(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="salary")
    price = models.DecimalField(max_digits=10, decimal_places=2) 
 
    def __str__(self):
        return self.user.username


class salaryattribute(models.Model):
    reason = models.CharField(max_length=100)
    amount = models.IntegerField()
    status = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="salaryttributes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    

class Bonus(models.Model):
    amount =  models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.amount


def query_deductionsIncentives_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    date_search = kwargs.get('date', None)[0]
    user_value = kwargs.get('user', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
   
    if order == 'desc':
        order_column = '-' + order_column

    queryset = salaryattribute.objects.all()
    total = queryset.count()
    

    
    # # '2025-09-30'
    # #print(month)

    if date_search:
        selected_date = datetime.strptime(date_search,'%Y-%m-%d')
        year = selected_date.year
        month = selected_date.month
        queryset = queryset.filter(created_at__year=year,created_at__month=month) 
    

    # if gender_value:
    #     queryset = queryset.filter(gender__icontains=gender_value)  

    if user_value:
        queryset = queryset.filter(user_id=user_value)             
                                        
                                          

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }
