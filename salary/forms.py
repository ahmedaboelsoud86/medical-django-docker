from  django.forms import ModelForm # type: ignore
from .models import Bonus
from  django import forms # type: ignore


class BonusForm(ModelForm):
   
    class Meta:
        model = Bonus
        fields = '__all__'

    amount = forms.CharField(required=True,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "type" : "number",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Amount',
    }))
    use_required_attribute = None    
        #fields = ['customer','product']

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if Branch.objects.filter(name=name).exists():
    #         raise forms.ValidationError('A  Branch name already exists.')
    #     return name    
