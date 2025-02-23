from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm, UserRegisterForm
# Create your views here.

def home(request):
    posts = Post.objects.all().select_related('author').all()
    return render(request, 'posts/home.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
            return render(request, 'posts/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'posts/register.html', {'form': form})

@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'posts/profile.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    post.delete()
    return redirect('profile')