from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('register/', views.register, name='register'),
    path('create/', views.post_create, name='post_create'),
    path('edit/<slug:slug>/', views.post_edit, name='post_edit'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('robots.txt', views.robots_txt),
]
