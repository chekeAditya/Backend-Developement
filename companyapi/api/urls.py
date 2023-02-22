from django.contrib import admin
from django.urls import include, path
from api.views import CompanyViewSet,EmployeeViewSet
from rest_framework import routers

#here we will create a router which will help us to create a route to the application
router = routers.DefaultRouter()
router.register(r'companies',CompanyViewSet)
router.register(r'employees',EmployeeViewSet)

urlpatterns = [
    path('' , include(router.urls))
]   

#here it will take the path from companies so coz of that we have put it as blank