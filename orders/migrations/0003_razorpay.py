# Generated by Django 4.0.4 on 2022-06-10 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderproduct_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='RazorPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razor_pay', models.CharField(max_length=200)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]