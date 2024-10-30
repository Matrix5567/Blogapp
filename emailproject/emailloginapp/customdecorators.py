from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import UserPermissions



def role_required():
    def decorator(view_func):
        @login_required()
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_admin:
                return HttpResponse("You do not have the required role.")
            return view_func(request, *args, **kwargs)
        return wrapper

    return decorator

def permission_required(perm):
    def decorator(view_func):
        @login_required()
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            permissions = UserPermissions.objects.all()
            has_permission = False
            for permission in permissions:
                if perm in permission.permissions.permissionnames:
                    has_permission = True
                    break
            if not has_permission:
                return HttpResponse("You don't have permission to view this page")
            return view_func(request, *args, **kwargs)
        return wrapper

    return decorator