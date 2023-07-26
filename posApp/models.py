from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
# Create  models here.

'''
class User(AbstractUser):
    groups = models.ManyToManyField(User)
    user_permissions = models.ManyToManyField('self')'''

class Department(models.Model):
    department_name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name_plural = 'Departments'
        permissions = (("delete_department", "can delete any department"),)
        permissions = (("save_department", "can save a department"),)

    def __str__(self):
        return self.department_name

class Position(models.Model):
    position_name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name_plural = 'Positions'
        permissions = (("delete_position", "can delete any position"),)
        permissions = (("save_position", "can save a position"),)

    def __str__(self):
        return self.position_name


class Employee(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, blank=True)
    firstname = models.TextField()
    middlename = models.TextField(blank=True, null=True)
    lastname = models.TextField()
    gender = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    contact = models.TextField()
    address = models.TextField()
    email = models.TextField()
    department_name = models.TextField(blank=True, null=True)
    position_name = models.TextField(blank=True, null=True)
    salary = models.FloatField(default=0)
    status = models.IntegerField()
    image = models.ImageField(upload_to='static/employee_images/', blank=True, null=True)  # New image field
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name_plural = 'Employees'

class EmployeeBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="employee")
    
class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name_plural = 'Categories'
        permissions = (("delete_category", "can delete any category"),)
        permissions = (("save_category", "can save a category"),)

    def __str__(self):
        return self.name

class Products(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    cost = models.FloatField(default=0)
    price = models.FloatField(default=0)
    status = models.IntegerField(default=1)
    quantity = models.IntegerField(default=0) 
    image = models.ImageField(upload_to='static/product_images/', blank=True, null=True)  # New image field
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name_plural = 'Products'
        permissions = (("delete_product", "can delete any product"),)
        permissions = (("save_product", "can save a product"),)

    def __str__(self):
        return self.code + " - " + self.name 

class ProductBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="products")
        
class Expences(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    amount = models.FloatField(default=0)
    quantity = models.IntegerField(default=0) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name_plural = 'Expences'
        permissions = (("delete_expense", "can delete any expence"),)
        permissions = (("save_expence", "can save a expence"),)

    def __str__(self):
        return self.code + " - " + self.name

class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    class Meta:
            verbose_name_plural = 'Sales'
            permissions = (("delete_sale", "can delete any sale"),)
            permissions = (("save_sale", "can save a sale"),)
            
    def __str__(self):
        return self.code

class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    tcost = models.FloatField(null=True, default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
