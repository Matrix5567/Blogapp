from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField(null=True)
    image = models.ImageField(upload_to='images/',null=True)
    is_admin = models.BooleanField(default=False,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    def __str__(self):
        return self.email


class Blog(models.Model):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='blogs')
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.ManyToManyField(CustomUser,related_name='liked_blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.likes.count()

    def has_user_liked(self,user):
        return user in self.likes.all()













