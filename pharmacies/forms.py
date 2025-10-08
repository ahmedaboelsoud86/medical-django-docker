from  django.forms import ModelForm # type: ignore
from .models import Pharmacy
from  branches.models import Branch
from  tools.models import Tool
from  django import forms # type: ignore
from django.db.models import Q

class PharmacyForm(ModelForm):
    tool = forms.ModelChoiceField(
        queryset=Tool.objects.all(),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.IntegerField(required=True,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "type" : "number",
        "autocomplete": "off",
        'maxlength' : 10000000,
        
    }))
    use_required_attribute = None
    
    class Meta:
        model = Pharmacy
        #fields = '__all__'
        fields = ['amount','tool','branch',]


    def clean(self):
        cleaned_data = super().clean()
        tool = cleaned_data.get('tool')
        branch = cleaned_data.get('branch')
        pk = cleaned_data.get('pk')

        if tool and branch:
            if Pharmacy.objects.filter(tool=tool, branch=branch).filter(pk=pk).exists():
                raise forms.ValidationError("Pharmacy with this Branch and Tool already exists")
        return cleaned_data    

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if pharmacy.objects.filter(name=name).exists():
    #         raise forms.ValidationError('A  pharmacy name already exists.')
    #     return name    
