from django import template
from ..models import Blog
from django.conf import settings

register = template.Library()

@register.filter(name = 'has_liked')
def has_liked(blog,user):
    return blog.has_user_liked(user)

