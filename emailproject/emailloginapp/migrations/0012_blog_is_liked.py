# Generated by Django 4.2.15 on 2024-08-26 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0011_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_liked',
            field=models.BooleanField(default=False, null=True),
        ),
    ]