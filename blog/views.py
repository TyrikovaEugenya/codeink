import time
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.db import IntegrityError
from .models import Post, Tag
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, RegisterForm, PostForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:post_list')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})

def post_list(request, tag_slug=None):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])    

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'tag': tag
    })

def post_detail(request, slug):
    print("=== post_detail called ===")
    post = get_object_or_404(Post, slug=slug, is_published=True)
    print(f"Post found: {post.title}")
    comments = post.comments.filter(is_approved=True)
    print(f"Approved comments: {comments.count()}")
    comments = post.comments.filter(is_approved=True)
    
    client_ip = get_client_ip(request)
    cache_key = f'comment_lock_{client_ip}_{post.id}'
    if cache.get(cache_key):
        form = None
        rate_limited = True
    else:
        rate_limited = False
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.is_approved = False
                try:
                    comment.save()
                    cache.set(cache_key, True, 60 * 5)
                    form = CommentForm()
                except IntegrityError:
                    form.add_error(None, "Ошибка сохранения комментария. Попробуйте снова.")       
        else:
            form = CommentForm()
    
    
        
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'rate_limited': rate_limited,
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Привязываем автора
            post.save()
            form.save_m2m()  # Для ManyToMany (теги)
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
        
    return render(request, 'blog/post_create.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if post.author != request.user:
        raise Http404("У вас нет прав на редактирование этой статьи.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = timezone.now()  # обновим время
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    # Получаем только опубликованные статьи автора
    posts = Post.objects.filter(
        author=user,
        is_published=True
    ).order_by('-created_at')

    return render(request, 'blog/user_profile.html', {
        'profile_user': user,  # чтобы не путать с request.user
        'posts': posts,
    })

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "",
        "Sitemap: https://codeink.onrender.com/sitemap.xml",  # ← замени на свой домен позже
        "Host: codeink.onrender.com"  # ← нестандартно, но Yandex понимает
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Вспомогательная функция для получения IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip