# Generated by Django 3.2.13 on 2022-07-04 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='stock_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
