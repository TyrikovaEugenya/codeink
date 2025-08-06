from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter
def markdownify(text):
    """
    Преобразует Markdown-текст в безопасный HTML
    """
    # extensions — поддержка списков, ссылок, кода и т.д.
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # подсветка кода
        'markdown.extensions.toc',         # оглавление
    ]
    html = markdown.markdown(text, extensions=extensions)
    return mark_safe(html)