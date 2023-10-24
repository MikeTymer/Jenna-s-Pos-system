# Generated by Django 4.2.4 on 2023-08-16 08:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('status', models.IntegerField(default=1)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'permissions': (('save_category', 'can save a category'),),
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.TextField()),
                ('description', models.TextField()),
                ('status', models.IntegerField(default=1)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Departments',
                'permissions': (('save_department', 'can save a department'),),
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100)),
                ('firstname', models.TextField()),
                ('middlename', models.TextField(blank=True, null=True)),
                ('lastname', models.TextField()),
                ('gender', models.TextField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, help_text='Please use the following format: <em>YYYY-MM-DD</em>.', null=True)),
                ('contact', models.TextField()),
                ('address', models.TextField()),
                ('email', models.TextField()),
                ('department_name', models.TextField(blank=True, null=True)),
                ('position_name', models.TextField(blank=True, null=True)),
                ('salary', models.FloatField(default=0)),
                ('status', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/employee_images/')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='EmployeeBulkUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('csv_file', models.FileField(upload_to='employee')),
            ],
        ),
        migrations.CreateModel(
            name='ProductBulkUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('csv_file', models.FileField(upload_to='Products')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('cost', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('quantity', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/product_images/')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.category')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'permissions': (('save_product', 'can save a product'),),
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('sub_total', models.FloatField(default=0)),
                ('grand_total', models.FloatField(default=0)),
                ('tax_amount', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('tendered_amount', models.FloatField(default=0)),
                ('amount_change', models.FloatField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Sales',
                'permissions': (('save_sale', 'can save a sale'),),
            },
        ),
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='posApp.products')),
                ('sales', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='posApp.sales')),
            ],
        ),
        migrations.CreateModel(
            name='salesItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('tcost', models.FloatField(default=0, null=True)),
                ('qty', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.products')),
                ('sale_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.sales')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.TextField()),
                ('description', models.TextField()),
                ('status', models.IntegerField(default=1)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='posApp.department')),
            ],
            options={
                'verbose_name_plural': 'Positions',
                'permissions': (('save_position', 'can save a position'),),
            },
        ),
        migrations.CreateModel(
            name='Expences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('amount', models.FloatField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.category')),
            ],
            options={
                'verbose_name_plural': 'Expences',
                'permissions': (('save_expence', 'can save a expence'),),
            },
        ),
    ]
