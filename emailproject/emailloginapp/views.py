from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse , JsonResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from . forms import SignupForm , LoginForm ,UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .validators import validate_blog
from.models import Blog , CustomUser , LikeButtonStatus
from django.contrib.sessions.models import Session
from django.db.models import Q
from .customdecorators import role_required



# Create your views here.
@login_required()
def members(request):
    blogs = Blog.objects.annotate(like_count=Count('likes'))
    for blog in blogs:
        like_status = LikeButtonStatus.objects.filter(person=request.user,blog=blog)
        for status in like_status:
            blog.is_liked = status.status
    return  render(request,'page1.html',{'posts':blogs})


@login_required()
def user_success(request):
    return  render(request,'success.html')



# signup page
def user_signup(request):
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
def create_blog(request):
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
def my_blog(request):
    posts = Blog.objects.filter(author=request.user)
    return render(request, 'myblogs.html',{'posts':posts})



@login_required
def delete_blog(request,id):
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
def edit_blog(request,id):
    posts = Blog.objects.get(id=id)
    if request.method == 'POST':
        posts.title = request.POST.get('title')
        posts.content = request.POST.get('content')
        posts.save()
        return redirect('my')
    return render(request, 'edit.html', {'posts': posts})

@login_required()
def search(request):
    search = request.GET.get('search')
    request.session['previous_url'] = request.build_absolute_uri()
    results = Blog.objects.filter(Q(title__icontains=search)| Q(content__icontains=search) |
                                      Q(author__first_name__icontains=search))
    return render(request, 'page1.html', {'posts': results})


@login_required()
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
def ad_min(request):
    authors_blogs = CustomUser.objects.select_related().\
        annotate(num_blogs=Count('blogs')).order_by(
        'num_blogs')
    return  render(request,'admin.html',{'details':authors_blogs})


@role_required()
def del_user(request,id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('ad_min')
    name = user.first_name + user.last_name
    return render(request, 'deleteblog.html', {'blog': name})

@role_required()
def lock_user(request,id):
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
        return JsonResponse({'count': post.likes.count(),'status':likebutton.status})









