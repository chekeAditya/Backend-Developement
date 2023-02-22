from rest_framework import serializers
from api.models import Company
from api.models import Employee

#create serializers here


class CompanySerializer(serializers.HyperlinkedModelSerializer) :
    #here we are using HyperlinkedModelSerializer coz in this we can create Meta class and inside that we can define our model
    company_id = serializers.ReadOnlyField() #used only for read purpose only
    class Meta :
        model = Company
        fields = "__all__" #add all the data of models


class EmployeeSerializer(serializers.HyperlinkedModelSerializer) :
    id = serializers.ReadOnlyField()
    class Meta :
        model = Employee
        fields = "__all__"
