import django_filters
from posApp.models import *
  
       
class DepartmentFilter(django_filters.FilterSet):    
    department_name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.NumberFilter(lookup_expr='gt')
    date_added = django_filters.DateFilter(lookup_expr='gt')
    date_updated = django_filters.DateFilter(lookup_expr='gt')
    
    class Meta:
        model = Department
        fields = ['department_name', 'description', 'status', 'date_added', 'date_updated' ]
        

    
class PositionFilter(django_filters.FilterSet):
    position_name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.NumberFilter(lookup_expr='gt')
    date_added = django_filters.DateFilter(lookup_expr='gt')
    date_updated = django_filters.DateFilter(lookup_expr='gt')
    
    class Meta:
        model = Position
        fields = ['position_name', 'description', 'status', 'date_added', 'date_updated' ]

class EmployeeFilter(django_filters.FilterSet):
    code = django_filters.NumberFilter(lookup_expr='gt')
    firstname = django_filters.CharFilter(lookup_expr='icontains')
    middlename = django_filters.CharFilter(lookup_expr='icontains')
    lastname = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.CharFilter(lookup_expr='icontains')
    dob = django_filters.CharFilter(lookup_expr='icontains')
    contact = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    
    date_hired = django_filters.TimeFilter(lookup_expr='icontains') 
    salary = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.NumberFilter(lookup_expr='gt') 


    class Meta:
        model = Employee
        fields = ['code', 'firstname', 'middlename', 'lastname', 'gender', 'dob', 'contact', 'address', 'email', 'date_hired', 'salary', 'status' ]
    
class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
   
    class Meta:
        model = Category
        fields = ['name' ]

class ProductsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter(lookup_expr='gt')
    
    class Meta:
        model = Products
        fields = [ 'name', 'price' ]
        
        
        
class ExpencesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    amount = django_filters.NumberFilter(lookup_expr='gt')
    
    class Meta:
        model = Expences
        fields = [ 'name', 'amount' ]