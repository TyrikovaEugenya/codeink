from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog:post_detail', args=[obj.slug])