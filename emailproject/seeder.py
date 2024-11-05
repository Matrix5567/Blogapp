import os
import django

os.environ['DJANGO_SETTINGS_MODULE']='emailproject.settings'
django.setup()

from emailloginapp.models import CustomUser



password = 'master1234master'  # ADMIN PASSWORD FOR ADMIN LOGIN
email='master@gmail.com'       # ADMIN EMAIL FOR  ADMIN LOGIN

if not CustomUser.objects.filter(email=email):
    is_admin = CustomUser.objects.create_user(
    email=email,
    password=password,
    first_name='Admin',
    last_name='User',
    address='kottayam',
    phone_number=9562045501,
    username='master',
    is_admin=True,
    is_active=True,
    )
    is_admin.save()
    print("admin created successfully")
else:
    print("admin user already exists")

