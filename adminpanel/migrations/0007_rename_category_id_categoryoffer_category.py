# Generated by Django 3.2.13 on 2022-06-27 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0006_auto_20220627_1128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryoffer',
            old_name='category_id',
            new_name='category',
        ),
    ]