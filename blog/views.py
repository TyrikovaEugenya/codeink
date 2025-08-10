import time
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.db import IntegrityError
from .models import Post, Tag
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login
from .forms import CommentForm, RegisterForm

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
    post = get_object_or_404(Post, slug=slug, is_published=True)
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