# Generated by Django 2.2.10 on 2021-11-08 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asking', '0002_auto_20211108_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswers',
            name='user_asking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asking.AskingModel'),
        ),
    ]