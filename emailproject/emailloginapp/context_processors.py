from .models import UserPermissions


def permission_context(request):
    permissions = UserPermissions.objects.all()
    return {'permission':permissions}