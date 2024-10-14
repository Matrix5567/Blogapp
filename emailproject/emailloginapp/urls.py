from django.urls import path
from . import views

urlpatterns = [
    path('' , views.user_login , name='login'),
    path('signup/' , views.user_signup , name='signup'),
    path('logout/' , views.user_logout , name='logout'),
    path('success/' , views.user_success , name='success'),
    path('createblog/' , views.create_blog , name='create'),
    path('myblog/' , views.my_blog , name='my'),
    path('myblog/deleteblog/<int:id>' , views.delete_blog , name='delete'),
    path('myblog/editblog/<int:id>' , views.edit_blog , name='edit'),
    path('members/', views.members, name='members'),
    path('members/like/<int:id>', views.liked , name='liked'),
    path('search/like/<int:id>' , views.liked , name='liked'),
    path('search/' , views.search , name='search'),
    path('profile/', views.profile_edit, name='profile_edit'),
    path('ad/', views.ad_min, name='ad_min'),
    path('ad/delete_user/<int:id>', views.del_user, name='del_user'),
]

