# Generated by Django 4.2.15 on 2024-10-21 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0028_remove_likebuttonstatus_post_blog_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='status',
        ),
        migrations.AddField(
            model_name='likebuttonstatus',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='emailloginapp.blog'),
        ),
        migrations.AlterField(
            model_name='likebuttonstatus',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='button_staus', to=settings.AUTH_USER_MODEL),
        ),
    ]