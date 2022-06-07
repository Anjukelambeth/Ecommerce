# Generated by Django 4.0.4 on 2022-06-06 23:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_useraddresses_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(error_messages={'required': 'Please let us know what to call you!'}, max_length=50, validators=[django.core.validators.RegexValidator(message='Enter a valid name', regex='^[A-Za-z][A-Za-z ]*$'), django.core.validators.MinLengthValidator(3, 'Min 3 char required')]),
        ),
    ]
