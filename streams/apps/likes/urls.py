from django.urls import path
from .views import like_comment

urlpatterns = [
    path('comment/comment:<int:comment_id>/', like_comment, name='like_comment'),
]
