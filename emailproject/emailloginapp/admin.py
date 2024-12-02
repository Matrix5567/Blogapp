from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , Blog , LikeButtonStatus , AllPermissionsList , UserPermissions\
    , Comments , Notifications , Forgotpassword

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Blog)
admin.site.register(LikeButtonStatus)
admin.site.register(AllPermissionsList)
admin.site.register(UserPermissions)
admin.site.register(Comments)
admin.site.register(Notifications)
admin.site.register(Forgotpassword)