from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from streams.apps.accounts.views import (
    create_account,
)

from streams.apps.streams.views import (
    get_streams,
    # get_posts_for_stream,
)

from streams.apps.profiles.views import (
    get_profile,
    get_my_profile,
    search_profiles,
)

from streams.apps.likes.views import (
    like_post,
    unlike_post,
    like_comment,
    delete_all_likes,
    get_post_likes_for_account,
    get_comment_likes_for_account,
)

from streams.apps.posts.views import (
    get_posts_for_account,
)

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # auth
    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refreshLogin', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verifyLogin', TokenVerifyView.as_view(), name='token_verify'),
    # account
    path('api/createAccount', create_account, name='create_account'),
    # profile
    path('api/getProfile', get_profile, name='get_profile'),
    path('api/getMyProfile', get_my_profile, name='get_my_profile'),
    path('api/searchProfiles', search_profiles, name='search_profiles'),
    # streams
    path('api/getStreams', get_streams, name='get_streams'),
    # posts
    # path('api/getPostsForStream', get_posts_for_stream, name='get_posts_for_stream'),
    path('api/getPostsForAccount', get_posts_for_account, name='get_posts_for_account'),
    # likes
    # path('api/likePost', like_post, name='like_post'),
    # path('api/unlikePost', unlike_post, name='unlike_post'),
    # path('api/likeComment', like_comment, name='like_comment'),
    # path('api/deleteAllLikes', delete_all_likes, name='delete_all_likes'),
    # path('api/getPostLikesForAccount', get_post_likes_for_account, name='get_post_likes_for_account'),
    # path('api/getCommentLikesForAccount', get_comment_likes_for_account, name='get_comment_likes_for_account'),
]
