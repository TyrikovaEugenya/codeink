from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('register/', views.register, name='register'),
    path('create/', views.post_create, name='post_create'),
    path('robots.txt', views.robots_txt),
]
