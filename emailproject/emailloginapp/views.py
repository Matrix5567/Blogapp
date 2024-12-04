from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse , JsonResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from . forms import SignupForm , LoginForm ,UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .validators import validate_blog
from.models import Blog , CustomUser , LikeButtonStatus , AllPermissionsList , UserPermissions, Comments \
    , Notifications , Forgotpassword
from django.contrib.sessions.models import Session
from django.db.models import Q
from .customdecorators import role_required , permission_required
from .email import send_mail_page , check_internet_connection
from .otpgeneration import otp


@login_required()      # all blog listing and search blogs
@permission_required('see_all_blogs')
def members(request):
    search = request.GET.get('search')
    if not search:
        blogs = Blog.objects.annotate(like_count=Count('likes'))
        for blog in blogs:
            like_status = LikeButtonStatus.objects.filter(person=request.user,blog=blog)
            comment = Comments.objects.filter(blog=blog)
            blog.comments = []
            for comments in comment:
                comment_dict = {
                    'blog_comments': comments.comments,
                    'comment_posted_user':comments.user.first_name,
                    'comment_posted_user_image':comments.user.image
                }
                blog.comments.append(comment_dict)
            for status in like_status:
                blog.is_liked = status.status
        return render(request,'page1.html',{'posts':blogs})
    else:
        request.session['previous_url'] = request.build_absolute_uri()
        results = Blog.objects.filter(Q(title__icontains=search)| Q(content__icontains=search) |
                                             Q(author__first_name__icontains=search))
        for result in results:
            like_status = LikeButtonStatus.objects.filter(person=request.user, blog=result)
            comment = Comments.objects.filter(blog=result)
            result.comments = []
            for comments in comment:
                comment_dict = {
                    'blog_comments': comments.comments,
                    'comment_posted_user': comments.user.first_name,
                    'comment_posted_user_image': comments.user.image
                }
                result.comments.append(comment_dict)
            for status in like_status:
                result.is_liked = status.status
        return render(request, 'page1.html', {'posts': results})



@login_required()
def user_success(request):  # user dashboard
    return  render(request,'success.html')


def user_signup(request): #user signup
    if request.method == 'POST':
        form = SignupForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_admin:
                    login(request, user)
                    request.session['user'] = email
                    request.session.save()
                    return redirect('ad_min')
                else:
                    locked = CustomUser.objects.get(email=email)
                    if locked.is_locked:
                        messages.error(request, 'THIS ACCOUNT IS LOCKED BY ADMIN...')
                    else:
                        login(request, user)
                        request.session['user'] = email
                        request.session.save()
                        return redirect('success')
            else:
                messages.error(request, 'INVALID LOGIN CREDENTIALS')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    Session.objects.filter(session_key=request.session.session_key)
    return redirect('login')


@login_required()
@permission_required('create_blog')
def create_blog(request):  # blog creation
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        errors = validate_blog(title, content)
        if errors:
            return render(request, 'create.html' , {'error':errors})
        blog = Blog(title=title,content=content,author=request.user)
        blog.save()
        return redirect('my')
    return render(request, 'create.html')

@login_required()
@permission_required('see_my_blogs')
def my_blog(request):  # blog by userid
    posts = Blog.objects.filter(author=request.user)
    return render(request, 'myblogs.html',{'posts':posts})



@login_required()
@permission_required('detele_blog')
def delete_blog(request,id):  # delete blog
    try:
        blog = Blog.objects.get(id=id)
        if request.method == 'POST':
            blog = Blog.objects.get(id=id)
            blog.delete()
            return redirect('my')
        return render(request, 'deleteblog.html', {'blog': blog})
    except Exception as e:
        return redirect('my')

@login_required()
@permission_required('edit_blog')
def edit_blog(request,id):  # edit blog
    posts = Blog.objects.get(id=id)
    if request.method == 'POST':
        posts.title = request.POST.get('title')
        posts.content = request.POST.get('content')
        posts.save()
        return redirect('my')
    return render(request, 'edit.html', {'posts': posts})


@login_required()  # edit userprofile
@permission_required('edit_user_profile')
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@role_required()
def ad_min(request):  # admin dashboard
    authors_blogs = CustomUser.objects.select_related().\
        annotate(num_blogs=Count('blogs')).order_by(
        'num_blogs')
    return  render(request,'admin.html',{'details':authors_blogs})


@role_required()
def del_user(request,id):  # user deletion by admin
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('ad_min')
    name = user.first_name + user.last_name
    return render(request, 'deleteblog.html', {'blog': name})

@role_required()
def lock_user(request,id):     # user locking by admin
    user = CustomUser.objects.get(id=id)
    if user.is_locked:
        user.is_locked = False
        user.save()
        return HttpResponse('User UnLocked')
    else:
        user.is_locked = True
        user.save()
        return HttpResponse('User Locked')


@login_required()
def test(request,id):                      # like/dislike
    post = Blog.objects.get(id=id)
    if post.has_user_liked(request.user):
        post.likes.remove(request.user)
        likebutton = LikeButtonStatus(person=request.user,blog=post,status=False)
        likebutton.save()
        return JsonResponse({'count': post.likes.count(),'status':likebutton.status})
    else:
        post.likes.add(request.user)
        likebutton = LikeButtonStatus(person=request.user, blog=post, status=True)
        likebutton.save()
        notification = Notifications(sender=request.user, receiver=post.author, post=post, notification_type='like')
        notification.save()
        return JsonResponse({'count': post.likes.count(),'status':likebutton.status})

@role_required()  # displaying permissions
def permission(request):
    allpermissions = AllPermissionsList.objects.select_related()
    for p in allpermissions:
        permission = UserPermissions.objects.filter(permissions=p)
        for status in permission:
            p.status=status.button_status
    return render(request,'permission.html',{'permissions':allpermissions})


@role_required() #setting permissions
def setpermission(request,id):
    fetchpermission = AllPermissionsList.objects.get(id=id)
    permission = UserPermissions.objects.filter(permissions=id)
    if not permission:
        UserPermissions(is_admin=False, permissions=fetchpermission, button_status=True).save()
        return JsonResponse({'data':'PERMISSION ADDED'})
    else:
        permission.delete()
        return JsonResponse({'data': 'PERMISSION DELETED'})


@login_required()
@permission_required('view_post_comments')
def comments(request):  #post comment
    blog_id = request.POST.get('blogid')
    post = Blog.objects.get(id=blog_id)
    comment = request.POST.get('comments')
    this_comment=Comments(blog=post,user=request.user,comments=comment)
    this_comment.save()
    notification = Notifications(sender=request.user, receiver=post.author, post=post, notification_type='comment')
    notification.save()
    return JsonResponse({'id':blog_id,'image':request.user.image.url,'comment':comment,'name':request.user.first_name})

@login_required()
def fetch_notification(request):    # showing notifications
    message = []
    notification = Notifications.objects.filter(receiver=request.user)
    if not notification:
        msg = "NO NOTIFICATIONS"
        dict = {
            'data': msg
        }
        message.append(dict)
    for noti in notification:
        if noti.notification_type == 'like':
            msg = f"{noti.sender.first_name + noti.sender.last_name} has liked your post '{noti.post.title}'"
            dict={
                'data':msg,
                'readstatus':noti.read,
            }
            message.append(dict)
        else:
            msg = f"{noti.sender.first_name + noti.sender.last_name} has commented on your post '{noti.post.title}'"
            dict = {
                'data': msg,
                'readstatus': noti.read,
            }
            message.append(dict)
    return JsonResponse({"data": message})

@login_required()   # marking read in notification for normal users
def mark_notification(request):
    Notifications.objects.filter(receiver=request.user).update(read=True)
    return JsonResponse({'success': True})


def login_check_user(request): # onload checking if admin or normal user to prevent unwanted ajax call
    if request.user.is_admin:
        return JsonResponse({"data":True})
    else:
        return JsonResponse({"data": False})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            if check_internet_connection():
                try:
                    send_mail_page(email=email)                            # function call to send email
                finally:
                    return JsonResponse({'data': True})
            else:
                return JsonResponse({'message': "CHECK YOUR INTERNET CONNECTION"})
        else:
            return JsonResponse({'message': "EMAIL NOT REGISTERED IN THE APP"})
    return render(request,'forgotpassword.html')

def forgot_login(request):  #forgot password login
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            get_user = Forgotpassword.objects.get(otp=otp)
            if otp == get_user.otp:
                login(request, get_user.user)
                get_user.delete()
                return redirect('success')
            else:
                messages.error(request, 'INVALID OTP')
                return render(request, 'forgotpassword.html')
        except:
            messages.error(request, 'INVALID OTP')
            return render(request, 'forgotpassword.html')

