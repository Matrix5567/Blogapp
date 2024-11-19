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
    path('profile/', views.profile_edit, name='profile_edit'),
    path('ad/', views.ad_min, name='ad_min'),
    path('ad/delete_user/<int:id>', views.del_user, name='del_user'),
    path('lock/<int:id>/',views.lock_user,name='lock_user'),
    path('test/<int:id>/',views.test,name='test'),
    path('permission', views.permission, name='permission'),
    path('setpermission/<int:id>/',views.setpermission,name='setpermission'),
    path('comments/',views.comments,name='comments'),
    path('fetchnotification/',views.fetch_notification,name='fetch_notification'),
    path('mark-notification-read/',views.mark_notification,name="mark_notification"),
    path('login-check-user/',views.login_check_user,name='login_check_user'),
]

