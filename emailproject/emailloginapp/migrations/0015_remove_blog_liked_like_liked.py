# Generated by Django 4.2.15 on 2024-08-26 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0014_blog_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='liked',
        ),
        migrations.AddField(
            model_name='like',
            name='liked',
            field=models.BooleanField(null=True),
        ),
    ]
