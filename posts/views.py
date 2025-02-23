from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm, UserRegisterForm
from django.db.models import Q

def home(request):
    posts = Post.objects.all()

    # Filtering
    date_order = request.GET.get('date_order', 'newest')  # Default is newest first
    media_type = request.GET.get('media_type', 'all')
    user_filter = request.GET.get('user', '')

    if date_order == 'oldest':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')

    if media_type == 'text_only':
        posts = posts.filter(image__isnull=True)
    elif media_type == 'images_only':
        posts = posts.filter(image__isnull=False)

    if user_filter:
        posts = posts.filter(author__username=user_filter)

    # Searching
    query = request.GET.get('q', '')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    context = {'posts': posts}
    return render(request, 'posts/home.html', context)

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

    # Filtering
    date_order = request.GET.get('date_order', 'newest')  # Default is newest first
    media_type = request.GET.get('media_type', 'all')

    if date_order == 'oldest':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')

    if media_type == 'text_only':
        posts = posts.filter(image__isnull=True)
    elif media_type == 'images_only':
        posts = posts.filter(image__isnull=False)

    # Searching
    query = request.GET.get('q', '')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    context = {'posts': posts}
    return render(request, 'posts/profile.html', context)


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