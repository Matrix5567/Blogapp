from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , Blog , Likebuttonstatus

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Blog)
admin.site.register(Likebuttonstatus)