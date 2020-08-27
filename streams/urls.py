from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    # TokenRefreshView,
    TokenVerifyView,
)

from streams.apps.accounts.views import (
    MyTokenObtainPairView,
    MyTokenRefreshView,
    create_account,
    get_account,
    update_account,
    delete_account,
)

from streams.apps.streams.views import (
    get_stream,
    create_stream,
    update_stream,
    delete_stream,
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
    get_followers_for_stream,
    get_following_for_stream,
)

from streams.apps.likes.views import (
    like_post,
    unlike_post,
    get_all_post_likes,
)

from streams.apps.posts.views import (
    get_post,
    get_posts_for_stream,
    get_posts_for_profile,
    get_explore,
)

from streams.apps.comments.views import (
    create_post_comment,
    get_comments_for_post,
    get_new_comments_for_post,
    get_new_comments_for_post_count,
)

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # auth
    path('api/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refreshLogin', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('api/verifyLogin', TokenVerifyView.as_view(), name='token_verify'),
    # account
    path('api/createAccount', create_account, name='create_account'),
    path('api/getAccount', get_account, name='get_account'),
    path('api/updateAccount', update_account, name='update_account'),
    path('api/deleteAccount', delete_account, name='delete_account'),
    # profile
    path('api/getProfile', get_profile, name='get_profile'),
    path('api/getMyProfile', get_my_profile, name='get_my_profile'),
    path('api/searchProfiles', search_profiles, name='search_profiles'),
    # streams
    path('api/getStream', get_stream, name='get_stream'),
    path('api/getStreamsForProfile', get_streams_for_profile, name='get_streams_for_profile'),
    path('api/createStream', create_stream, name='create_stream'),
    path('api/updateStream', update_stream, name='update_stream'),
    path('api/deleteStream', delete_stream, name='delete_stream'),
    # posts
    path('api/getPost', get_post, name='get_post'),
    path('api/getPostsForStream', get_posts_for_stream, name='get_posts_for_stream'),
    path('api/getPostsForProfile', get_posts_for_profile, name='get_posts_for_profile'),
    path('api/getExplore', get_explore, name='get_explore'),
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
    path('api/getFollowersForStream', get_followers_for_stream, name='get_followers_for_stream'),
    path('api/getFollowingForStream', get_following_for_stream, name='get_following_for_stream'),
    # likes
    path('api/likePost', like_post, name='like_post'),
    path('api/unlikePost', unlike_post, name='unlike_post'),
    path('api/getAllPostLikes', get_all_post_likes, name='get_all_post_likes'),
    # comments
    path('api/createPostComment', create_post_comment, name='create_post_comment'),
    path('api/getCommentsForPost', get_comments_for_post, name='get_comments_for_post'),
    path('api/getNewCommentsForPost', get_new_comments_for_post, name='get_new_comments_for_post'),
    path('api/getNewCommentsForPostCount', get_new_comments_for_post_count, name='get_new_comments_for_post_count'),
]
