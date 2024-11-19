import os
import django

os.environ['DJANGO_SETTINGS_MODULE']='emailproject.settings'
django.setup()

from emailloginapp.models import AllPermissionsList

names = ['create_blog','detele_blog','edit_blog','see_my_blogs','see_all_blogs','edit_user_profile',
         'view_post_comments','view_notifications']

permissions = AllPermissionsList.objects.all()
for name in names:
    if not AllPermissionsList.objects.filter(permissionnames = name).exists():
        AllPermissionsList.objects.create(permissionnames=name)
print("PERMISSIONS CREATED")