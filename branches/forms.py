from  django.forms import ModelForm # type: ignore
from .models import Branch
from  django import forms # type: ignore


class BranchForm(ModelForm):
    name = forms.CharField(required=True,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Branch Name',
        }))
    use_required_attribute = None
    
    class Meta:
        model = Branch
        fields = '__all__'
        #fields = ['customer','product']

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if Branch.objects.filter(name=name).exists():
    #         raise forms.ValidationError('A  Branch name already exists.')
    #     return name    
