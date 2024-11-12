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
    phone_number = models.IntegerField(null=True,unique=True)
    image = models.ImageField(upload_to='images/',null=True)
    is_admin = models.BooleanField(default=False,null=True)  # role admin = True , normal user =False
    is_locked = models.BooleanField(default=False,null=True)
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


class LikeButtonStatus(models.Model):
    person = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    status = models.BooleanField(default=False,null = True)

class Comments(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    comments = models.CharField(max_length=255)

class AllPermissionsList(models.Model):
    permissionnames = models.CharField(max_length=20)

class UserPermissions(models.Model):
    is_admin = models.BooleanField(null=True)  # role false for normal users
    permissions = models.ForeignKey(AllPermissionsList,on_delete=models.CASCADE,null=True)
    button_status = models.BooleanField(default=False,null=True)


class Notifications(models.Model):
    NOTIFICATION_TYPES = (
        ('like','Like'),
        ('comment','Comment')
    )

    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sent_notifications')
    receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='received_notifications')
    notification_type = models.CharField(max_length=10,choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Blog,on_delete=models.CASCADE,null=True)
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE,null=True)
    read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.read = True
        self.save()



