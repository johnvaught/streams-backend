from django.urls import path
from .views import \
    create_post, \
    read_public_post, \
    read_public_posts_for, \
    update_post, \
    delete_post

app_name = 'posts'
urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('read/<int:post_id>/', read_public_post, name='read_public_post'),
    path('read/<str:handle>/', read_public_posts_for, name='read_public_posts_for'),
    path('update/<int:post_id>/', update_post, name='update_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
]
