# ****Django Rest API Course****

1. Install Python, Django and DRF
2. Set up Django Models
3. Set up Serializers
4. Setup views → request, response
5. Setup Urls → /about
6. Test your Api’s

**Steps:**

- Firstly Start a project using :- `django-admin startproject companyapi`
- Create `[view.py](http://view.py)` file

```python
from django.http import HttpResponse, JsonResponse

def home_page(request):
    print("Aditya")
    friends = [
        "Aditya",
        "Shivom",
        "Kunal",
        "Pawan"
    ]
    return JsonResponse(friends,safe = False)
```

- `python3 [manage.py](http://manage.py/) runserver` used to run the server
- Install DRF → `pip3 install djangorestframework`
- Add `'rest_framework’` in INSTALLED_APPS

```python
# Use Django's standard `django.contrib.auth` permissions,
# or allow read-only access for unauthenticated users.
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

- Create App Called API → `python3 manage.py startapp api`
- Create [`model.py`](http://model.py) class, in this we will be defining all the data which we need in a model class

```python
from django.db import models

#Creating Company Model
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    about = models.TextField()
    type = models.CharField(max_length=100,choices=
            (('IT','IT'),
            ('Non It','Non It'),
            ('Mobile Phones','Mobile Phones')
            ))
    added_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    

#Employee Model
```

- Create `serializer.py`

```python
from rest_framework import serializers
from api.models import Company

#create serializers here

class CompanySerializer(serializers.HyperlinkedModelSerializer) :
    #here we are using HyperlinkedModelSerializer coz in this we can create Meta class and inside that we can define our model
    class Meta :
        model = Company
        fields = "__all__"
 #add all the data of models
```

- Now create a class `views.py`

```python
from django.shortcuts import render
from rest_framework import viewsets
from api.models import Company
from api.serializers import CompanySerializer

# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
```

- Now create [`Urls.py`](http://Urls.py) → it will help us to provide the route between the app’s

```python
from django.contrib import admin
from django.urls import include, path
from api.views import CompanyViewSet
from rest_framework import routers

#here we will create a router which will help us to create a route to the application
router = routers.DefaultRouter()
router.register(r'companies',CompanyViewSet)

urlpatterns = [
    path('' , include(router.urls))
]   

#here it will take the path from companies so coz of that we have put it as blank
```

- Add the path of [`urls.py`](http://urls.py) (company_level) to `urls.py` (api)

```python
from django.contrib import admin
from django.urls import include, path

from companyapi.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home_page),
    path('api/v1/', include('api.urls'))
]
```

- Go to `[settings.py](http://settings.py)` add `‘api'` to **INSTALLED_APPS**

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
		'api',
    'rest_framework',
]
```

- Do the migration command → `python3 [manage.py](http://manage.py/) makemigrations`
- Migrate project to sqlite3 → `python3 [manage.py](http://manage.py/) migrate`

Migration successlly completed now you can see it in DbSqliteDb

- Now you can run the server → `python3 manage.py runserver`
- If you want to see the company name then in that case you use this in serializers
    
    `company_id = serializers.ReadOnlyField() #used only for read purpose only`
    
- From here Now you can perform the CRED Operation

Now let’s create a **`Employee Model`**

```python
from django.db import models

#Creating Company Model
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    about = models.TextField()
    type = models.CharField(max_length=100,choices=
            (('IT','IT'),
            ('Non It','Non It'),
            ('Mobile Phones','Mobile Phones')
            ))
    added_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    

#Employee Model
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    about = models.CharField(max_length=50)  
    position = models.CharField(max_length= 50,choices=(
        ('Manager','manager'),
        ('Software Developer','sd'),
        ('Project Leader', 'pl')
    ))
    company = models.ForeignKey(Company,on_delete= models.CASCADE) #here foreign key will create a relation with company
```

- Create `Serializers`

```python
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
```

- Create `Views`

```python
from django.shortcuts import render
from rest_framework import viewsets
from api.models import Company,Employee
from api.serializers import CompanySerializer,EmployeeSerializer

# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

#This function will call the {companies_id} employee
#company/{companyId}/employees
    #here pk -> primarkKey
   @action(detail = True, methods = ['get'])
    def employees(self,request,pk=None):
        company = Company.objects.get(pk=pk)
        emps = Employee.objects.filter(company=company)
        emps_serializer = EmployeeSerializer(emps , many = True , context = {'request': request})
        return Response(emps_serializer.data)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
```

- Now the company will show the list of all companies, but it’s in the form of Company Object(1), Company Object (2), etc to return the name of the specific company use

```python
#this function is used to return the name of the company
    def __str__(self) -> str:
        return self.name + '--' +self.location
```

- If you have to connect comany and employe the use

```python
#This function will call the {companies_id} employee
#company/{companyId}/employees
    #here pk -> primarkKey
   @action(detail = True, methods = ['get'])
    def employees(self,request,pk=None):
        company = Company.objects.get(pk=pk)
        emps = Employee.objects.filter(company=company)
        emps_serializer = EmployeeSerializer(emps , many = True , context = {'request': request})
        return Response(emps_serializer.data)
```

- **[to disable admin-style browsable interface of django-rest-framework?](https://stackoverflow.com/questions/11898065/how-to-disable-admin-style-browsable-interface-of-django-rest-framework)**

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    #with this user can not run api on the browser
     'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
```

- Now let’s configure Admin, to insert data, delete data and many more in `admin.py`

```python
from django.contrib import admin
from api.models import Company,Employee

# Register your models here.
admin.site.register(Company)
admin.site.register(Employee)
```

- Now to perform all these task you have to create a superUser using `python3 manage.py createsuperuser`
- Now you can login into it and can perform the CRUD operation
- Let’s customise the admin panel
