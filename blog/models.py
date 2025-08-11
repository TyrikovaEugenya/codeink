from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from pytils.translit import translify

class Post(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор"
    )
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
            slug_text = translify(self.title)
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = f'post-{self.id}' if self.pk else f'temp-{hash(self.title)}'
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
    

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Статья"
    )
    author = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email", max_length=254, blank=True, null=True)
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    is_approved = models.BooleanField("Одобрен", default=False)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if self.pk:
            old_comment = Comment.objects.get(pk=self.pk)
            just_approved = not old_comment.is_approved and self.is_approved
        else:
            just_approved = False
            
        super().save(*args, **kwargs)
        
        if just_approved:
            try:
                send_mail(
                    subject=f'Ваш комментарий опубликован — {self.post.title}',
                    message=f'''
Здравствуйте, {self.author}!

Ваш комментарий к статье "{self.post.title}" был одобрен и опубликован.

Спасибо за участие в обсуждении!

С уважением,
Команда CodeInk
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Ошибка отправки email: {e}")

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post.title}'
    