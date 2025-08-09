from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Слаг", unique=True, blank=True)
    content = models.TextField("Контент (Markdown)")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    is_published = models.BooleanField("Опубликовано", default=False)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    

class Tag(models.Model):
    name = models.CharField("Название", max_length=50, unique=True)
    slug = models.SlugField("Слаг", unique=True, blank=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    