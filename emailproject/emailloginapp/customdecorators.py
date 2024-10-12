from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse




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