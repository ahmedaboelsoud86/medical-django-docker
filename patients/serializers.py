from django.conf import settings
from rest_framework import serializers
from .models import Patient,Expense
from branches.models import Branch
from patients.models import Appointment

class BranchSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=True, read_only=False)
    class Meta:
        model=Branch
        fields='__all__'


class PatientSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    branch_field = serializers.SerializerMethodField()
    class Meta:
        model=Patient
        fields=['id','branch_id','branch','branch_field','title','email','mobile','job','birthday','adress','gender','height','weight']

    def get_branch_field(self, obj):
        # 'obj' is the instance of MyModel being serialized
        # Perform any calculations or data retrieval here
        return f"{obj.branch}"


class AppointmentSerializer(serializers.ModelSerializer):
    #patients = PatientSerializer(many=True, read_only=True)
    #patient = serializers.PrimaryKeyRelatedField(read_only=True)
    patient = serializers.StringRelatedField(read_only=True)
 
    class Meta:
        model= Appointment
        fields=['id','patient']


class ExpenseSerializer(serializers.ModelSerializer):
    patient_field = serializers.SerializerMethodField()
    tool_field = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d") 
    class Meta:
        model=Expense
        #fields='__all__'
        fields=['id','patient_field','tool_field','amount','created_at']
        #fields=['id','branch_id','branch','branch_field','title','email','mobile','job','birthday','adress','gender','height','weight']

    def get_patient_field(self, obj):
        # 'obj' is the instance of MyModel being serialized
        # Perform any calculations or data retrieval here
        return f"{obj.patient}" 
     
    def get_tool_field(self, obj):
        # 'obj' is the instance of MyModel being serialized
        # Perform any calculations or data retrieval here
        return f"{obj.tool}"        






