# Generated by Django 4.2.1 on 2023-07-18 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesitems',
            name='tcost',
            field=models.FloatField(default=0),
        ),
    ]
