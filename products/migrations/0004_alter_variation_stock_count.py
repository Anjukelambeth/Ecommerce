# Generated by Django 3.2.13 on 2022-07-04 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_variation_stock_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='stock_count',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]
