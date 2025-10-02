from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
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
    return render(request, 'create-account.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')  # Using .get() is safer
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            # Render the login page again to show the error
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES) # Handles files
        if form.is_valid():
            post = form.save(commit=False)
            # Assign the user object directly (assumes Post.author is a ForeignKey)
            post.author = request.user
            post.save()
            messages.success(request, "Post created!")
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-date_posted')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'post_detail.html', context)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if post.author != request.user:  # Avoid notifying yourself
            Notifications.objects.create(
                user=User.objects.get(username=post.author),  # Notify the post's author
                message=f"{request.user.username} liked your post."
            )

    return redirect('post_detail', pk=post.id)

@login_required
def share_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user not in post.shares.all():
        post.shares.add(request.user)
        if post.author != request.user:
            Notifications.objects.create(
                user=post.author,
                message=f"{request.user.username} shared your post."
            )
    return redirect('home')



@login_required
def notifications_view(request):
    notifications = Notifications.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'notifications.html', {'notifications': notifications})

def search_results(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = Post.objects.filter(title__icontains=query)
    return render(request, "search_results.html", {"results": results, "query": query})

@login_required
def profile_view(request, username):
    # Get the user object for the username in the URL
    profile_user = get_object_or_404(User, username=username)
    
    # Get the profile linked to that user
    profile = get_object_or_404(Profile, user=profile_user)
    
    # Get all posts by that user
    user_posts = Post.objects.filter(author=profile_user).order_by('-date_posted')

    if request.method == 'POST':
        # Ensure the logged-in user can only edit their own profile
        if request.user == profile_user:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been updated successfully!")
                return redirect('profile', username=request.user.username)
    else:
        # For a GET request, show the form pre-filled with existing data
        form = ProfileForm(instance=profile)
        
    context = {
        'profile': profile,
        'posts': user_posts,
        'form': form,
    }
    return render(request, 'profile.html', context)