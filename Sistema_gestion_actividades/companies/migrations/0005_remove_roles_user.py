# Generated by Django 4.2.1 on 2023-06-13 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_company_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roles',
            name='user',
        ),
    ]
