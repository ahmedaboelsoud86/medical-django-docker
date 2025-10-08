from django.db import models
from django.db.models import Q
from django.core.validators import MinLengthValidator,MaxLengthValidator
from branches.models import Branch
from tools.models import Tool
from model_utils import Choices
from django.conf import settings
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver


ORDER_COLUMN_CHOICES = Choices(
	('0', 'id'),
	('1', 'title'),
	('2', 'branch'),
	('3', 'mobile'),
	('4', 'email'),
)

ORDER_COLUMN_EXPENSE_CHOICES = Choices(
	('0', 'amount'),
	('1', 'patient'),
	('2', 'tool'),
)

class Patient(models.Model):

	CHOICES_GENDER = {
		"ma": "Male",
		"fa": "Female",
	}
	branch   = models.ForeignKey(Branch, related_name='branch', on_delete=models.CASCADE,null=True)
	title    = models.CharField(max_length=100, validators=[MaxLengthValidator(limit_value=100, message="Title is too tooo!")])
	email    = models.EmailField(unique=True) 
	mobile   = models.CharField(max_length=30, validators=[MaxLengthValidator(limit_value=40, message="phone is too tooo!")])    
	job      = models.CharField(max_length=100, validators=[MaxLengthValidator(limit_value=100, message="Job is too tooo!")])    
	birthday = models.DateField(null=True,blank=True)
	adress   = models.CharField(max_length=100, blank=True,null=True)
	gender   = models.CharField(max_length=10, choices=CHOICES_GENDER)
	height   = models.SmallIntegerField(blank=True,null=True)
	weight   = models.SmallIntegerField(blank=True,null=True)

	def __str__(self):
		return self.title

	class Meta:
		db_table = "patient"

def query_patients_by_args(**kwargs):
	draw = int(kwargs.get('draw', None)[0])
	length = int(kwargs.get('length', None)[0])
	start = int(kwargs.get('start', None)[0])
	search_value = kwargs.get('search[value]', None)[0]
	title_value = kwargs.get('title', None)[0]
	gender_value = kwargs.get('gender', None)[0]
	branch_value = kwargs.get('branch', None)[0]
	order_column = kwargs.get('order[0][column]', None)[0]
	order = kwargs.get('order[0][dir]', None)[0]

	order_column = ORDER_COLUMN_CHOICES[order_column]
   
	if order == 'desc':
		order_column = '-' + order_column

	queryset = Patient.objects.all()
	total = queryset.count()
	
	
	# if search_value:
	  
	#    queryset = queryset.filter(Q(id__icontains=search_value) |
	#                                    Q(title__icontains=search_value) 
	#                                    )
  

	if title_value:
		queryset = queryset.filter(title__icontains=title_value) 

	if gender_value:
		queryset = queryset.filter(gender__icontains=gender_value)  

	if branch_value:
		queryset = queryset.filter(branch_id=branch_value)             
										
										  

	count = queryset.count()
	queryset = queryset.order_by(order_column)[start:start + length]
	return {
		'items': queryset,
		'count': count,
		'total': total,
		'draw': draw
	}


class Appointment(models.Model):
	doctor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, related_name='appointments', on_delete=models.CASCADE,null=True)
	medicine = models.CharField(max_length=100, null=True,blank=True, validators=[MaxLengthValidator(limit_value=100, message="Title is too tooo!")])
	note = models.TextField(blank=True,null=True)
	appdata = models.DateField()

	class Meta:
		db_table = 'appointments' 
		#permissions = [
		 #   ("can_deleteall_branches", "Can delete all branches"),
		#]

	def __str__(self):
		#return self.doctor.username + self.patient.name
		return(f"Doctor :  ( {self.doctor.username} )  With Patient : ( {self.patient.title} ) .")


def query_appointment_by_args(**kwargs):
	doctor_value = kwargs.get('doctor', None)[0]
	appdata_value = kwargs.get('appdata', None)[0]
	
	queryset = Appointment.objects.all()

	if doctor_value:
		queryset = queryset.filter(doctor_id=doctor_value) 

	if appdata_value:
		queryset = queryset.filter(appdata=appdata_value)     

	return {
		'items': queryset,    
	}


class Expense(models.Model):
	tool = models.ForeignKey(Tool, related_name='expenses', on_delete=models.CASCADE,null=True)
	patient = models.ForeignKey(Patient, related_name='expenses', on_delete=models.CASCADE,null=True)
	amount = models.IntegerField()
	created_at =  models.DateTimeField(auto_now=True)


def query_expense_by_args(**kwargs):
	draw = int(kwargs.get('draw', None)[0])
	length = int(kwargs.get('length', None)[0])
	start = int(kwargs.get('start', None)[0])
	order_column = kwargs.get('order[0][column]', None)[0]
	order = kwargs.get('order[0][dir]', None)[0]
	#search_value = kwargs.get('search[value]', None)[0]
	tool_value = kwargs.get('tool', None)[0]
	patient_value = kwargs.get('patient', None)[0]
	#gender_value = kwargs.get('gender', None)[0]
	

	order_column = ORDER_COLUMN_EXPENSE_CHOICES[order_column]
   
	if order == 'desc':
		order_column = '-' + order_column

	queryset = Expense.objects.all()
	total = queryset.count()
	

	if patient_value:
		queryset = queryset.filter(patient_id=patient_value)  

	if tool_value:
		queryset = queryset.filter(tool_id=tool_value)             
										
										  

	count = queryset.count()
	queryset = queryset.order_by(order_column)[start:start + length]
	return {
		'items': queryset,
		'count': count,
		'total': total,
		'draw': draw
	}



class Profit(models.Model):
	price = models.DecimalField(max_digits=10, decimal_places=2)
	appointment = models.ForeignKey(Appointment, related_name='profits', on_delete=models.CASCADE,null=True)
	created_at =  models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'profits' 
		#permissions = [
		 #   ("can_deleteall_branches", "Can delete all branches"),
		#]


class Ray(models.Model):
	patient = models.ForeignKey(Patient, related_name='rays', on_delete=models.CASCADE,null=True)
	photo = models.ImageField(upload_to='uploads/',null=True,blank=True)
	
	class Meta:
		db_table = 'rays'
  
  
	# def delete(self, *args, **kwargs):
	# 	if self.photo:
	# 		if os.path.isfile(self.photo.path):
	# 			os.remove(self.photo.path)
	# 	super().delete(*args, **kwargs)
  
	# def delete(self, *args, **kwargs):
	# 	if self.photo:
	# 		if os.path.isfile(self.photo.path):
	# 			os.remove(self.photo.path)
	# 	super().delete(*args, **kwargs)

@receiver(pre_delete, sender=Ray)
def delete_image_on_model_delete(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)

