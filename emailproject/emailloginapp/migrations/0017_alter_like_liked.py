# Generated by Django 4.2.15 on 2024-08-26 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0016_alter_like_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='liked',
            field=models.IntegerField(null=True),
        ),
    ]
