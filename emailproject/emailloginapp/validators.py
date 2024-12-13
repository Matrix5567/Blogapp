import smtplib

from django.core.exceptions import ValidationError
from . models import CustomUser



def validate_phone_number(phone):
   if len(str(phone)) <10 or len(str(phone))>12:
       raise ValidationError('phone number must be 10 digits or 12 digits')



def validate_blog(title,content):
    if not title:
        return 'Title cannot be empty'
    elif not content:
        return 'Content cannot be empty'


def validate_image(image):
    extensions = ['jpg','png']
    if image.size > 5*1024*1024:
        raise ValidationError('image size must be less than 5mb')
    elif image.name.split('.')[-1].lower() not in extensions:
        raise ValidationError("format not allowed")

