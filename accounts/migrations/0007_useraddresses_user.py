# Generated by Django 4.0.4 on 2022-06-05 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_useraddresses_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddresses',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
