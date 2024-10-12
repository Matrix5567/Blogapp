from django.conf import settings
from django.http import HttpResponse
import datetime
from django.contrib.auth import logout


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.MAINTENANCE_MODE:
            return HttpResponse("Site under maintenance", status=503)
        return self.get_response(request)

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
         if request.user.is_authenticated:
             current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             last_activity = request.session.get('last_activity', None)
             if last_activity:
                 last_activity = datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
                 if (datetime.datetime.now() - last_activity).seconds > 500:
                     logout(request)
             request.session['last_activity'] = current_time
         return self.get_response(request)


