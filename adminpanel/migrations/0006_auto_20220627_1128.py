# Generated by Django 3.2.13 on 2022-06-27 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_variation'),
        ('category', '0002_alter_category_slug'),
        ('adminpanel', '0005_alter_productoffer_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoffer',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.category'),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_offer', to='products.products'),
        ),
    ]
