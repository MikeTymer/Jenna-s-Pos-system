from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from flask import jsonify
from posApp.models import *
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
import json, sys
from datetime import date, datetime
from posApp.filters import *
from django.db import transaction
import csv
from django.core.files.storage import default_storage 

              
# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='Login is a success'
            else:
                resp['msg'] = "The username or password you entered is incorrect, please try again"
        else:
            resp['msg'] = "The username or password you entered is incorrect, please try again"
    return HttpResponse(json.dumps(resp),content_type='application/json')
    #return render(request, 'pos/login.html')
#Logout
def logout_user(request):
    logout(request)
    return redirect('/')

# Create your views here.
@login_required
def home(request):
  
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    employees = len(Employee.objects.all())
    departments = len(Department.objects.all())
    positions = len(Position.objects.all())
    #cost = Sales.objects.filter(cost = id).first()
    

    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    #sale_id = salesItems.objects.get(sale_id=sale_id).all()
    today_Expences = len(Expences.objects.all())
    
    total_sales = sum(today_sales.values_list('grand_total',flat=True))
    # 600000
    tocost = 300000
   
    profit = total_sales - tocost
    
    context = {
        'page_title':'Home',
        'today_Expences': today_Expences,
        'categories' : categories,
        'products' : products,
        'employees' : employees,
        'departments' : departments,
        'positions'  : positions,
        'transaction' : transaction,
        'total_sales' : total_sales,
        'tocost' : tocost,
        'profit': profit,
    }
    
    #profit = sum(today_sales.values_list('grand_total', flat=True))
    return render(request, 'pos/home.html',context)


def about(request):
    context = {
        'page_title':'About',
    }
    return render(request, 'pos/about.html',context)

#Department
@login_required
def department(request):
  
    queryset = Department.objects.all()
    departmentfilter = DepartmentFilter(request.GET, queryset=Department.objects.all())
    filtered_objects = departmentfilter.qs

    department_list = queryset
    # department_list = {}
    context = {
        'page_title':'Department List',
        'department':department_list,
        'filter': departmentfilter, 
        'objects': filtered_objects,
    }
    return render(request, 'pos/department.html',context )

@login_required
@permission_required('department.manage_department')
def manage_department(request):
    department = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            department = Department.objects.filter(id=id).first()
    
    context = {
        'department' : department  
    }
    return render(request, 'pos/manage_department.html', context)

@login_required

#def save_department(request):
#  data =  request.POST
#    resp = {'status':'failed'}
#    try:
#        if (data['id']).isnumeric() and int(data['id']) > 0 :
#            save_department= Department.objects.filter(id = data['position_name']).update(name=data['department_name'], description = data['description'],status = data['status'])
#        else:
#            save_department = Department(name=data['department_name'], description = data['description'],status = data['status'])
#            save_department.save()
#        resp['status'] = 'success'
#        messages.success(request, 'Department Successfully saved.')
#    except:
#        resp['status'] = 'failed'
#    return HttpResponse(json.dumps(resp), content_type="application/json")

def save_department(request):
    data = request.POST
    resp = {'status': 'failed'}
    
    try:
        if 'id' in data and data['id'].isnumeric() and int(data['id']) > 0:
            department = Department.objects.get(id=data['id'])
            department.department_name = data['department_name']
            department.description = data['description']
            department.status = data['status']
            department.save()
        else:
            department = Department(
                department_name=data['department_name'],
                description=data['description'],
                status=data['status']
            )
            department.save()
        
        resp['status'] = 'success'
        messages.success(request, 'Department successfully saved.')
    except:
        resp['status'] = 'failed'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required

def delete_department(request):
    data =  request.POST
    resp = {'status':''}
    try:
       Department.objects.filter(id = data['id']).delete()
       resp['status'] = 'success'
       messages.success(request, 'department Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


#Position
@login_required
def position(request):
    queryset = Position.objects.all()
    positionfilter = PositionFilter(request.GET, queryset=Position.objects.all())
    filtered_objects = positionfilter.qs
    
    position_list = queryset
    # position_list = {}
    context = {
        'page_title':'Position List',
        'position':position_list,
        'filter': positionfilter, 
        'objects': filtered_objects,
    }
    return render(request, 'pos/position.html',context)


@login_required
@permission_required('position.manage_position')
def manage_position(request):
    position = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            position = Position.objects.filter(id=id).first()
    
    context = {
        'position' : position
    }
    return render(request, 'pos/manage_position.html',context)

@login_required
@permission_required('position.save_position')
def save_position(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        position_id = data.get('id')
        position_name = data.get('position_name')
        description = data.get('description')
        status = data.get('status')

        if position_id and position_id.isnumeric() and int(position_id) > 0:
            position = Position.objects.filter(id=position_id).update(position_name=position_name, description=description, status=status)
        else:
            position = Position(position_name=position_name, description=description, status=status)
            position.save()

        resp['status'] = 'success'
        resp['message'] = 'Position successfully saved.'
    except Exception as e:
        resp['status'] = 'failed'
        resp['message'] = str(e)

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
@permission_required('position.delete_position')

def delete_position(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Position.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Position successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


#Employees
@login_required
def employee(request):
    queryset = Employee.objects.all()
    employeefilter = EmployeeFilter(request.GET, queryset=queryset)
    filtered_objects = employeefilter.qs
    
    employee_list = queryset
    # employee_list = {}
    context = {
        'page_title':'Employees List',
        'Employees':employee_list,
        'filter': employeefilter, 
        'objects': filtered_objects,
    }
    return render(request, 'pos/employee.html',context)

@login_required
def manage_employee(request):
    employee = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employee.objects.filter(id=id).first()
    
    context = {
        'employee' : employee
    }
    return render(request, 'pos/manage_employee.html',context)

@login_required
@permission_required('employee.save_employee')
def save_employee(request):
    save_employee = Employee()
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    
    if 'id' in data:
        id = data['id']
        code = data['code']
        
    if id.isnumeric() and int(id) > 0:
        check = Employee.objects.exclude(id=id).filter(code=code).all()
    else:
        check = Employee.objects.filter(code=code).all()
    if len(check) > 0 :
        resp['msg'] = "Employee Code Already Exists in the database"
    else:
       
        try:
            image_file = request.FILES.get('image')
            employee_id = data.get('id')
            code = data.get('code')
            firstname = data.get('firstname')
            middlename = data.get('middlename')
            lastname = data.get('lastname')
            gender = data.get('gender')
            dob = data.get('dob')
            contact = data.get('contact')
            address = data.get('address')
            email = data.get('email')
            department_name = data.get('department_name')
            position_name = data.get('position_name')
            salary = data.get('salary')
            status = data.get('status')

           
            if (data['id']).isnumeric() and int(data['id']) > 0 :
           
                save_employee = Employee.objects.get(id=employee_id)
                save_employee.code = code
                save_employee.firstname=firstname 
                save_employee.middlename = middlename 
                save_employee.lastname = lastname 
                save_employee.gender = gender
                save_employee.dob = dob
                save_employee.contact = contact 
                save_employee.address = address 
                save_employee.email = email
                save_employee.department_name= department_name
                save_employee.position_name = position_name 
                save_employee.salary = salary  
                save_employee.status = status
                
             
            if image_file:
                 
                # Delete old image file if exists                
               
                if save_employee.image:
                    default_storage.delete(save_employee.image.path)
                # Save new image file
                save_employee.image = image_file
                
                save_employee.save()
                
                    
            else:
               
                save_employee = Employee(
                code=code,
                firstname=firstname,
                middlename=middlename,
                lastname=lastname,
                gender=gender,
                dob=dob,
                contact=contact,
                address=address,
                email=email,
                department_name=department_name,
                position_name=position_name,
                salary=float(salary),
                status=status
                
            )
                                     
                if image_file:
                   
                    save_employee.image = image_file
            

            save_employee.save()
            resp['status'] = 'success'
            messages.success(request, 'Employee Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


def upload_employees(request):
    resp = {'status':''}
    try:
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            resp['status'] = 'success'
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
            next(csv_data)  # Skip the header row

            for row in csv_data:
                Employee.objects.create(
                    code=row[0],
                    firstname=row[1],
                    middlename=row[2],
                    lastname=row[3],
                    gender=row[4],
                    dob=row[5],
                    contact=row[6],
                    address=row[7],
                    email=row[8],
                    department_name=row[9],
                    position_name=row[10],
                    salary=row[11],
                    status=row[12],
                )
            resp['status'] = 'failed'
            messages.success(request, 'Employee csv data saved successfully')

    except KeyError:
        resp['status'] = 'failed'
        messages.success(request, 'Please upload a file and try again.')

    except Exception as e:
        resp['status'] = 'failed'
        messages.error(request, str(e))

    return redirect('employee-page')


@login_required
@permission_required('employee.delete_employee')
def delete_employee(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Employee.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Employee Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#Categories
@login_required
def category(request):
    
    queryset = Category.objects.all()
    categoryfilter = CategoryFilter(request.GET, queryset=queryset)
    filtered_objects = categoryfilter.qs
    
    category_list = queryset
    # category_list = {}
    context = {
        'page_title':'Category List',
        'category':category_list,
        'filter': categoryfilter, 
        'objects': filtered_objects,
    }
    return render(request, 'pos/category.html',context)

@login_required
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()
    
    context = {
        'category' : category
    }
    return render(request, 'pos/manage_category.html',context)

@login_required
@permission_required('category.save_category')
def save_category(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_category = Category.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_category = Category(name=data['name'], description = data['description'],status = data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@permission_required('product.delete_category')
def delete_category(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Category.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Products
@login_required
def products(request):
    queryset = Products.objects.all()
    productsfilter = ProductsFilter(request.GET, queryset=queryset)
    filtered_objects = productsfilter.qs
    
    product_list = queryset
    context = {
        'page_title':'Product List',
        'products':product_list,
        'filter': productsfilter, 
        'objects': filtered_objects
    }
    return render(request, 'pos/products.html',context)


@login_required
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()
    
    context = {
        'product' : product,
        'categories' : categories
    }
    return render(request, 'pos/manage_product.html',context)
def test(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'pos/test.html',context)
@login_required
@permission_required('product.save_product')  

#products remake
def save_product(request):
    product = Products()
    
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    
    image_file = request.FILES.get('image')
    
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.filter(code=data['code'], id=id).all()   # Products.objects.exclude(id=id).filter(code=data['code']).all()
        
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id = data['category_id']).first()
        
    
        try:
            
            print(image_file)
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                print("if")
              
                save_product = Products.objects.filter(id = data['id']).update(code=data['code'], category_id=category, name=data['name'], description = data['description'], cost = float(data['cost']),price = float(data['price']),status = data['status'],quantity = data['quantity'])
                
                #print(save_product.code)
                if image_file:
                    if product.image:
                        save_product.image = image_file 
                    
                        save_product.save()
                
                    
            else:
                print("else")
                save_product = Products(code=data['code'], category_id=category, name=data['name'], description = data['description'],cost = float(data['cost']), price = float(data['price']),status = data['status'],quantity = data['quantity'])
                
                if image_file:
                    
                    if product.image:
                        product.delete(product.image.path)
                    # Save new image file
                    
                        save_product.image = image_file                  
                        save_product.save()
                    
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except Exception as e:
            resp['status'] = 'failed'
            print(str(e))
            messages.error(request, str(e))
    return HttpResponse(json.dumps(resp), content_type="application/json")



@login_required
@permission_required('product.delete_product')
def delete_product(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Products.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#revised and working csv products upload 
def upload_products(request):
    resp = {'status':''}
    try:
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            resp['status'] = 'success'
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8')
            
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
            next(csv_data)  # Skip the header row

            for row in csv_data:
                print('for')
                Products.objects.create(
                    code=row[0],
                    category_id=Category.objects.get(name=row[1]),
                    name=row[2],
                    description=row[3],
                    price=row[4],
                    status=row[5],
                    quantity=row[6],
                   
                )
            category_id = Category.objects.get( name = 'Category' )
            resp['status'] = 'failed'
            messages.success(request, 'Product csv data saved successfully')

    except KeyError:
        resp['status'] = 'failed'
        messages.success(request, 'Please upload a proper csv file and try again.')

    except Exception as e:
        resp['status'] = 'failed'
        print(str(e))
        messages.error(request, str(e))

    return redirect('product-page')

@login_required

def pos(request):
    products = Products.objects.filter(status = 1)
    product_json = []
  
    for product in products:
        product_json.append({'id':product.id, 'name':product.name, 'price':float(product.price), 'cost': float(product.cost) })
    context = {
        'page_title' : "Point of Sale",
        'products' : products,
        'product_json' : json.dumps(product_json)
    }
    # return HttpResponse('')
    return render(request, 'pos/pos.html',context)
    

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    
    context = {
        'grand_total' : grand_total,
       
    }
    return render(request, 'pos/checkout.html',context)

@login_required
def save_pos(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    pref = datetime.now().year + datetime.now().year
    i = 1
    cost = 30000 #data.getlist('cost[]')[i]   
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        sales = Sales(code=code, sub_total = data['sub_total'], tax = data['tax'], tax_amount = data['tax_amount'], grand_total = data['grand_total'], tendered_amount = data['tendered_amount'], amount_change = data['amount_change']).save()
        sale_id = Sales.objects.last().pk
        i = 0
        
        for prod in data.getlist('product_id[]'):
            product_id = prod
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            price = data.getlist('price[]')[i]        
            qty = data.getlist('qty[]')[i] 
            tcost = int(qty) * float(cost)
            total = float(qty) * float(price)
            
            q2 = int(qty) - product.quantity
            
            
            print({'sale_id' : sale, 'product_id' : product, 'qty' : qty,'tcost':tcost,'price' : price, 'total' : total})
            salesItems(sale_id = sale,product_id = product,qty = qty,price = price,tcost = tcost,total = total).save()
            i += int(1)
            
            
            if product.quantity >= int(qty):
                product.quantity -= int(qty)
                
                product.save()
            else:
                    # Handle the case where the requested quantity exceeds the available quantity
                resp['msg'] = f"Insufficient quantity for product: {product.name}, you need {q2} more {product.name}s to make the purchase. Please add {q2} more {product.name}s to the quantity of the {product.name}s form"
                return HttpResponse(json.dumps(resp), content_type="application/json")       
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
        #print("Unexpected error:", sys.exc_info()[2])
    except Exception as e:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[1])
        messages.error(request, str(e))
    return HttpResponse(json.dumps(resp),content_type="application/json")


@login_required
def salesList(request):
    sales = Sales.objects.all()
    #tcost = len(salesItems.objects.all())
    #sq = len(salesItems.objects.all())
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale,field.name)
        data['items'] = salesItems.objects.filter(sale_id = sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']),'.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)
    context = {
        'page_title':'Sales Transactions',
        'sale_data':sale_data,
        #'sq':sq,
    }
    # return HttpResponse('')
    return render(request, 'pos/sales.html',context)


@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id = sales).all()
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }

    return render(request, 'pos/receipt.html',context)
    # return HttpResponse('')

@login_required
@permission_required('sale.delete_sale')
def delete_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id = id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')

# Expences
@login_required
def expences(request):
    queryset = Expences.objects.all()
    expecesfilter = ExpencesFilter(request.GET, queryset=Department.objects.all())
    filtered_objects = expecesfilter.qs
    
    expences_list = queryset
    context = {
        'page_title':'expences List',
        'expences': expences_list,
        'filter': expecesfilter, 
        'objects': filtered_objects
    }
    return render(request, 'pos/expences.html',context)

@login_required
def manage_expences(request):
    expence = {}
    categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            expence = Expences.objects.filter(id=id).first()
    
    context = {
        'expence' : expence,
        'categories' : categories
    }
    return render(request, 'pos/manage_expences.html',context)

def test(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'pos/test.html',context)

@login_required
@permission_required('product.save_product')
def save_expence(request):
    
    data =  request.POST
    resp = {'status':'failed'}
   
    category = Category.objects.filter(id=data['category_id']).first()
    if not category:
        raise Exception('Invalid category_id')
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_expence = Expences.objects.filter(id = data['id']).update(category_id=category, name=data['name'], description = data['description'], amount = float(data['amount']),quantity = data['quantity'])
        else:
            save_expence = Expences(category_id=category, name=data['name'], description = data['description'], amount = float(data['amount']),quantity = data['quantity'])
            save_expence.save()
        resp['status'] = 'success'
        messages.success(request, 'Expence Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")  

@login_required
@permission_required('product.delete_product')
def delete_expence(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Expences.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Expence Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


'''
def salesList(request):
    sales = Sales.objects.all()
    sq = len(Position.objects.all())
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale,field.name)
        data['items'] = salesItems.objects.filter(sale_id = sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']),'.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)
    context = {
        'page_title':'Sales Transactions',
        'sale_data':sale_data,
        'sq':sq,
    }
    # return HttpResponse('')
    return render(request, 'pos/sales.html',context)
'''


# charts and analytics

def product_chart(request):
    products = Product.objects.all()
    chart = chartit.BarChart(
        title="Products vs. Prices",
        x_axis_title="Products",
        y_axis_title="Prices",
        data=[
            (product.name, product.price) for product in products
        ],
    )
    return render(request, "chart.html", {"chart": chart})

