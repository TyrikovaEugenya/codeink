from django.shortcuts import render, get_object_or_404
from .models import Post, Tag
from django.http import HttpResponse

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
    return render(request, 'blog/post_detail.html', {'post': post})

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "",
        "Sitemap: https://codeink.onrender.com/sitemap.xml",  # ← замени на свой домен позже
        "Host: codeink.onrender.com"  # ← нестандартно, но Yandex понимает
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")