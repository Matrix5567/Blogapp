# Generated by Django 4.2.15 on 2024-08-28 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0022_remove_blog_likes_delete_like_blog_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_admin',
            field=models.BooleanField(default=False, null=True),
        ),
    ]