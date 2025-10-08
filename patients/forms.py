from  django.forms import ModelForm 
from  .models import Patient,Appointment,Expense, Ray
from  branches.models import Branch
from  django import forms
from  doctors.models import Doctor
from  tools.models import Tool
from  users.models import User
from django.utils import timezone
from datetime import datetime



class PatientForm(forms.ModelForm):
    CHOICES = [
        ('fa', 'FeMale'),
        ('ma', 'Male'),
   ]
    class Meta:
        model = Patient
        fields = '__all__'



    # def __init__(self,*args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance.pk:
    #         print(self.instance.pk)
    #         del self.fields['password']
    #         del self.fields['cpassword']

    title = forms.CharField(required=True,max_length=1000,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Name',
    }))
    job = forms.CharField(required=True,max_length=1000,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'job',
    }))
    adress = forms.CharField(required=True,max_length=1000,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Adress',
    }))
    email = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Email',
    }))
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mobile = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'type' : 'number',
    }))

    birthday = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'type' : 'date',
    }))


    weight = forms.IntegerField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'type' : 'number',
    }))
    height = forms.IntegerField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'type' : 'number',
    }))

    gender = forms.ChoiceField(
            label='status',
            choices=CHOICES,
            widget=forms.RadioSelect
    )
    
   
    use_required_attribute = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
            # Exclude the current instance's email from the check
        if self.instance and Patient.objects.filter(email=email).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("This email address is already in use by another Patient.")
        return email
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
            # Exclude the current instance's mobile from the check
        if self.instance and Patient.objects.filter(mobile=mobile).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("This mobile  is already in use by another Patient.")
        return mobile
    

   

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['doctor','doctor','note','appdata','patient']

    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(doctor__isnull=False),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control action',"id":"doctors"})
    )
    appdata = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control action",
        "id" : "appdata",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'type' : 'date',
    }))
    price = forms.IntegerField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'type' : 'number',
    }))
    use_required_attribute = None

    def clean_appdata(self):
        date_string = self.cleaned_data['appdata']
        appdata = datetime.strptime(date_string, "%Y-%m-%d").date()
        print(type(appdata))
        if appdata <= timezone.now().date():
            raise forms.ValidationError("Event date must be in the future.")
        return appdata  



class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = '__all__'
        #fields = ['amount','patient','tool','created_at']
    
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        empty_label="Select a Patient",
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tool = forms.ModelChoiceField(
        queryset=Tool.objects.all(),
        empty_label="Select a Tool",
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.IntegerField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'type' : 'number',
    }))
    use_required_attribute = None
    
    
class MyImageForm(forms.ModelForm):
    class Meta:
        model = Ray
        fields = ['photo']
    photo = forms.ImageField(widget=forms.FileInput(attrs={'id': 'images-post','name':'images[]'}))        