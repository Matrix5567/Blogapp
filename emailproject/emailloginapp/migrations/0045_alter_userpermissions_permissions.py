# Generated by Django 4.2.15 on 2024-10-26 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0044_alter_userpermissions_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpermissions',
            name='permissions',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
