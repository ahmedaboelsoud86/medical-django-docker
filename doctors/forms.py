from  django.forms import ModelForm 
from  .models import Doctor
from  branches.models import Branch
from  django import forms
from  users.models import User 




class UserForm(forms.ModelForm):
    CHOICES = [
        ('inactive', 'In active'),
        ('active', 'Active'),
   ]
    class Meta:
        model = User
        #exclude = ['password']
        fields = ['username','branche','email','phone','password','cpassword','status']



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
    status = forms.ChoiceField(
            label='status',
            choices=CHOICES,
            widget=forms.RadioSelect
    )
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
            raise forms.ValidationError("This Doctor name  is already in use by another user.")
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
            raise forms.ValidationError("This email address is already in use by another user.")
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
      
class DoctorForm(forms.ModelForm):
   
    class Meta:
        model = Doctor
        fields = ['photo','birthday','brief']
        #fields = []

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user_id:
            del self.fields['photo']
 
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    # photo = forms.CharField(required=False,
    #   widget=forms.TextInput(attrs={
     #   "type" : "file",   
      #  "class": "form-control",
       # "autocomplete": "off",
      #'maxlength' : 10000000,
       #}))
    birthday = forms.CharField(required=True,
       widget=forms.TextInput(attrs={
        "type" : "date",   
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
    }))
    
         
    #started_salary = forms.CharField(required=True,
    #   widget=forms.TextInput(attrs={
     #   "type" : "number",   
      #  "class": "form-control",
       # "autocomplete": "off",
        #'maxlength' : 10000000,
        #'placeholder' : 'Started Salary',
   #}))
    
    brief = forms.CharField(required=True,
       widget=forms.Textarea(attrs={   
        "class": "form-control",
        'maxlength' : 10000000,
        'placeholder' : 'Brief',
        "rows": 5,
        "style": "resize: none;"
    }))
    use_required_attribute = None
    
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check the content type of the uploaded file
            if photo.content_type != 'image/jpeg':
                raise forms.ValidationError("Only JPG photo are allowed.")
            return photo
    
   
   #fields = ['customer','product']

   
        
  
