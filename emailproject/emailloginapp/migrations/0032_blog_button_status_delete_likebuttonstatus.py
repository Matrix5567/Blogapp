# Generated by Django 4.2.15 on 2024-10-21 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0031_alter_likebuttonstatus_person_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='button_status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.DeleteModel(
            name='likebuttonstatus',
        ),
    ]
