# Generated by Django 4.2.15 on 2024-08-18 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0002_customuser_nickname_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.IntegerField(null=True),
        ),
    ]
