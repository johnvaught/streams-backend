from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from streams.apps.streams.views import (
    get_my_own_streams,
    get_streams_i_follow,
    get_posts_for_stream,
)


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # auth
    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refreshLogin', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verifyLogin', TokenVerifyView.as_view(), name='token_verify'),
    # streams apps
    # streams
    path('api/getMyOwnStreams', get_my_own_streams, name='get_my_own_streams'),
    path('api/getStreamsIFollow', get_streams_i_follow, name='get_streams_i_follow'),
    # posts
    path('api/getPostsForStream', get_posts_for_stream, name='get_posts_for_stream'),
    # tbd
    path('accounts/', include('streams.apps.accounts.urls')),
    path('profiles/', include('streams.apps.profiles.urls')),
    path('posts/', include('streams.apps.posts.urls')),
    path('streams/', include('streams.apps.streams.urls')),
    path('follows/', include('streams.apps.follows.urls')),
    path('comments/', include('streams.apps.comments.urls')),
    path('likes/', include('streams.apps.likes.urls')),
]
