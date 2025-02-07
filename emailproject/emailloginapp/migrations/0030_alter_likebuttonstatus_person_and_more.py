# Generated by Django 4.2.15 on 2024-10-21 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emailloginapp', '0029_remove_blog_status_likebuttonstatus_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likebuttonstatus',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='likebuttonstatus',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='button_status', to='emailloginapp.blog'),
        ),
    ]
