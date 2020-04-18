from django.urls import path
from .views import \
    comment_on_post, \
    comment_on_comment, \
    delete_comment, \
    get_comments_on_post, \
    get_comments_on_comment, \
    update_comment


urlpatterns = [
    path('post/create/', comment_on_post, name='comment_on_post'),
    path('comment/create/', comment_on_comment, name='comment_on_comment'),
    path('delete/', delete_comment, name='delete_comment'),
    path('post/post:<int:post_id>/', get_comments_on_post, name='get_comments_on_post'),
    path('comment/comment:<int:comment_id>/', get_comments_on_comment, name='get_comments_on_comment'),
    path('update/comment:<int:comment_id>/', update_comment, name='update_comment'),
]
