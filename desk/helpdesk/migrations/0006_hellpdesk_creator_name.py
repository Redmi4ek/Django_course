# Generated by Django 4.2.5 on 2023-10-02 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0005_hellpdesk_asigned_user_hellpdesk_confirmed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hellpdesk',
            name='creator_name',
            field=models.CharField(default='idontknow', max_length=255),
        ),
    ]