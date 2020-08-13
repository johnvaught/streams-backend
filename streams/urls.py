from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    # TokenRefreshView,
    TokenVerifyView,
)

from streams.apps.accounts.views import (
    create_account,
    MyTokenObtainPairView,
    MyTokenRefreshView
)

from streams.apps.streams.views import (
    get_streams_for_profile,
)

from streams.apps.profiles.views import (
    get_profile,
    get_my_profile,
    search_profiles,
)

from streams.apps.follows.views import (
    get_followers_for_profile,
    get_following_for_profile,
    get_followers_for_me,
    get_following_for_me,
    unfollow_profile_from_profile,
    unfollow_stream,
    unfollow_profile,
    follow_profile,
    follow_stream,
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
    get_posts_for_profile,
)

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # auth
    path('api/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refreshLogin', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('api/verifyLogin', TokenVerifyView.as_view(), name='token_verify'),
    path('api/createAccount', create_account, name='create_account'),
    # profile
    path('api/getProfile', get_profile, name='get_profile'),
    path('api/getMyProfile', get_my_profile, name='get_my_profile'),
    path('api/searchProfiles', search_profiles, name='search_profiles'),
    # streams
    path('api/getStreamsForProfile', get_streams_for_profile, name='get_streams_for_profile'),
    # posts
    # path('api/getPostsForStream', get_posts_for_stream, name='get_posts_for_stream'),
    path('api/getPostsForProfile', get_posts_for_profile, name='get_posts_for_profile'),
    # follows
    path('api/getFollowersForMe', get_followers_for_me, name='get_followers_for_me'),
    path('api/getFollowingForMe', get_following_for_me, name='get_following_for_me'),
    path('api/getFollowersForProfile', get_followers_for_profile, name='get_followers_for_profile'),
    path('api/getFollowingForProfile', get_following_for_profile, name='get_following_for_profile'),
    path('api/unfollowProfileFromProfile', unfollow_profile_from_profile, name='unfollow_profile_from_profile'),
    path('api/unfollowStream', unfollow_stream, name='unfollow_stream'),
    path('api/unfollowProfile', unfollow_profile, name='unfollow_profile'),
    path('api/followProfile', follow_profile, name='follow_profile'),
    path('api/followStream', follow_stream, name='follow_stream'),
    # likes
    # path('api/likePost', like_post, name='like_post'),
    # path('api/unlikePost', unlike_post, name='unlike_post'),
    # path('api/likeComment', like_comment, name='like_comment'),
    # path('api/deleteAllLikes', delete_all_likes, name='delete_all_likes'),
    # path('api/getPostLikesForAccount', get_post_likes_for_account, name='get_post_likes_for_account'),
    # path('api/getCommentLikesForAccount', get_comment_likes_for_account, name='get_comment_likes_for_account'),
]
