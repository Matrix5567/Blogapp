import smtplib
import time
import requests
import threading
from .otpgeneration import otp
from django.core.mail import send_mail
from django.conf import settings
from .models import Forgotpassword ,CustomUser


def check_internet_connection():  # checking internet connection
        try:
                requests.get("https://www.google.com",timeout=5)
                return True
        except requests.ConnectionError:
                return False

def timer(user,password):       # timer for otp expiration
        temp_save = Forgotpassword(user=user, otp=password)
        temp_save.save()
        seconds =  3 * 60
        for i in range(seconds,0,-1):
                time.sleep(1)
        temp_save.delete()

def send_mail_page(email):      # email sending
       address = email
       subject = "BLOG APP OTP"
       password = otp()
       message = f"Your one time otp is '{password}'"
       user = CustomUser.objects.get(email=email)
       send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
       timer_thread = threading.Thread(target=timer,args=(user,password,))  # to stop page refreshing until timer stops
       timer_thread.start()


def locked_or_not(email):             # to identify whether user is locked or not
    locked = CustomUser.objects.get(email=email)
    if locked.is_locked:
        return True
    else:
        return False

