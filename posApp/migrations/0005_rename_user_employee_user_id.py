# Generated by Django 4.2.1 on 2023-07-20 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0004_productbulkupload_employee_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='user',
            new_name='user_id',
        ),
    ]
