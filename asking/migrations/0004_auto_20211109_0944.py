# Generated by Django 2.2.10 on 2021-11-09 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asking', '0003_auto_20211108_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswers',
            name='user_asking',
        ),
        migrations.AddField(
            model_name='useranswers',
            name='asking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asking.AskingModel'),
        ),
        migrations.AddField(
            model_name='useranswers',
            name='userid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
