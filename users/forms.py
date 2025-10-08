from  django.forms import ModelForm 
from  branches.models import Branch
from  django import forms
from  .models import User 
from  django.contrib.auth.forms import UserCreationForm
from  salary.models import salaryattribute
from  salary.models import Salary





class SalaryForm(forms.ModelForm):
    user = forms.CharField(required=False) 

    class Meta:
        model = Salary
        fields = ['price']
    
    price = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "type" : "number",   
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : '',
    }))  
    
    use_required_attribute = None  
        

class UserForm(forms.ModelForm):
    CHOICES = [
        ('inactive', 'In active'),
        ('active', 'Active'),
   ]
    class Meta:
        model = User
        #exclude = ['password']
        fields = ['username','branche','email','phone','password','cpassword']



    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            print(self.instance.pk)
            del self.fields['password']
            del self.fields['cpassword']

    username = forms.CharField(required=True,max_length=1000,
       widget=forms.TextInput(attrs={
       "class": "form-control",
       "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Name',
    }))
    email = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        "type": "email",
        'maxlength' : 10000000,
        'placeholder' : 'Email',
    }))
    branche = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'phone',
    }))
   
    password = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "type" : "password",   
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : '',
    }))
    cpassword = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "type" : "password",   
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : '',
    }))
    use_required_attribute = None
    def clean_username(self):
        username = self.cleaned_data.get('username')
            # Exclude the current instance's username from the check
        if self.instance and User.objects.filter(username=username).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("This User name  is already in use by another user.")
        return username  
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('A  Email already exists.')
    #     return email
    def clean_email(self):
        email = self.cleaned_data.get('email')
            # Exclude the current instance's email from the check
        if self.instance and User.objects.filter(email=email).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("This Email address is already in use by another user.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
            # Exclude the current instance's phone from the check
        if self.instance and User.objects.filter(phone=phone).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("This phone  is already in use by another user.")
        return phone
    def clean(self):
      cleaned_data = super(UserForm, self).clean()
      password = cleaned_data.get("password")
      cpassword = cleaned_data.get("cpassword")

      if password != cpassword:
         self.add_error('cpassword', "Password does not match")

      return cleaned_data  
      

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','branche','email','phone','password1','password2']


class salaryAttributeForm(forms.ModelForm):
    CHOICES = [
        ('inactive', 'In active'),
        ('active', 'Active'),
    ]
    
    class Meta:
        model = salaryattribute
        fields = ['reason','amount','user','status']

    reason = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        "type": "text",
        'maxlength' : 10000000,
        'placeholder' : 'Reason',
    })) 
    amount = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        "type": "number",
        'maxlength' : 10000000,
        'placeholder' : 'Days',
    }))
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(doctor__isnull=True),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )    
    use_required_attribute = None

