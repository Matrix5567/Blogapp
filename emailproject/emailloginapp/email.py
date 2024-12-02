import time
import threading
from .otpgeneration import otp
from django.core.mail import send_mail
from django.conf import settings
from .models import Forgotpassword ,CustomUser


def timer(temp_save):
        seconds =  3 * 60
        for i in range(seconds,0,-1):
                time.sleep(1)
        temp_save.delete()

def send_mail_page(email):
        address = email
        subject = "BLOG APP OTP"
        message = f"Your one time otp is '{otp()}'"
        user = CustomUser.objects.get(email=email)
        temp_save = Forgotpassword(user = user,otp=otp())
        temp_save.save()
        send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
        timer_thread = threading.Thread(target=timer,args=(temp_save,))  # to stop page refreshing until timer stops
        timer_thread.start()

