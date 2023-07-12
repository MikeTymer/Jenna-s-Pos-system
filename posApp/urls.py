from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),
    path('login', auth_views.LoginView.as_view(template_name = 'posApp/login.html',redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logout_user, name="logout"),
    path('category', views.category, name="category-page"),
    path('manage_category', views.manage_category, name="manage_category-page"),
    path('save_category', views.save_category, name="save-category-page"),
    path('delete_category', views.delete_category, name="delete-category"),
    path('products', views.products, name="product-page"),
    path('manage_products', views.manage_products, name="manage_products-page"),
    path('test', views.test, name="test-page"),
    path('save_product', views.save_product, name="save-product-page"),
    path('delete_product', views.delete_product, name="delete-product"),
    path('pos', views.pos, name="pos-page"),
    path('checkout-modal', views.checkout_modal, name="checkout-modal"),
    path('save-pos', views.save_pos, name="save-pos"),
    path('sales', views.salesList, name="sales-page"),
    path('receipt', views.receipt, name="receipt-modal"),
    path('delete_sale', views.delete_sale, name="delete-sale"),
    path('employee', views.employee, name="employee-page"),
    path('manage_employee', views.manage_employee, name="manage_employee-page"),
    path('save_employee', views.save_employee, name="save-employee-page"),
    path('delete_employee', views.delete_employee, name="delete_employee"),
    path('department', views.department, name="department-page"),
    path('manage_department', views.manage_department, name="manage_department-page"),
    path('save-department', views.save_department, name="save-department-page"),
    path('delete_department', views.delete_department, name="delete-department"),
    path('position', views.position, name="position-page"),
    path('manage_position', views.manage_position, name="manage_position-page"),
    path('save-position', views.save_position, name="save-position-page"),
    path('delete_position', views.delete_position, name="delete-position"),
    path('upload_employees', views.upload_employees, name="upload_employees-page"),
    path('upload_products', views.upload_products, name="upload_products-page"),
    path('expences', views.expences, name="expence-page"),
    path('manage_expences', views.manage_expences, name="manage_expences-page"),
    path('test', views.test, name="test-page"),
    path('save_expence', views.save_expence, name="save-expence-page"),
    path('delete_expence', views.delete_expence, name="delete-expence"),
    
    
]