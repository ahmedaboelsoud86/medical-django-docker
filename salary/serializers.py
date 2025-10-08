from django.conf import settings
from rest_framework import serializers
from .models import salaryattribute




class deductionsIncentivesSerializer(serializers.ModelSerializer):
    user_field = serializers.SerializerMethodField()
    branch_field = serializers.SerializerMethodField()
    #tool_field = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d") 
    class Meta:
        model=salaryattribute
        #fields='__all__'
        fields=['id','reason','amount','status','user_field','created_at','branch_field']

    def get_user_field(self, obj):
        # 'obj' is the instance of MyModel being serialized
        # Perform any calculations or data retrieval here
        return f"{obj.user}" 
     
    def get_branch_field(self, obj):
        # 'obj' is the instance of MyModel being serialized
        # Perform any calculations or data retrieval here
        return f"{obj.user.branche}"        






