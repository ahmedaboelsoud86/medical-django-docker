from  django.forms import ModelForm # type: ignore
from .models import Tool
from  django import forms # type: ignore


class ToolForm(ModelForm):
    name = forms.CharField(required=True,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Tool Name',
        }))
    
    price = forms.IntegerField(required=True,
       widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'type' : 'number',
    }))
    use_required_attribute = None
    
    class Meta:
        model = Tool
        fields = '__all__'
        #fields = ['customer','product']

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if Tool.objects.filter(name=name).exists():
    #         raise forms.ValidationError('A  Tool name already exists.')
    #     return name    
