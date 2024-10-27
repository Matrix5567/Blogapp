from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , Blog , LikeButtonStatus , AllPermissionsList , UserPermissions

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Blog)
admin.site.register(LikeButtonStatus)
admin.site.register(AllPermissionsList)
admin.site.register(UserPermissions)