# Generated by Django 4.2.5 on 2023-09-20 01:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hellpdesk',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
