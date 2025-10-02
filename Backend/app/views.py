from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Profile, Notifications
from .forms import SignupForm, PostForm, CommentForm, ProfileForm


def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'home.html', {'posts': posts})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, bio="")
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            messages.success(request, "Post created!")
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            Notifications.objects.create(
                user=request.user,
                message=f"{request.user.username} commented on a post"
            )
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        Notifications.objects.create(
            user=request.user,
            message=f"{request.user.username} liked a post"
        )
    return redirect('post_detail', post_id=post.id)


@login_required
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user not in post.shares.all():
        post.shares.add(request.user)
        Notifications.objects.create(
            user=request.user,
            message=f"{request.user.username} shared a post"
        )
    return redirect('home')


@login_required
def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(author=username)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile', username=username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'form': form})


@login_required
def notifications_view(request):
    notifications = Notifications.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'notifications.html', {'notifications': notifications})
