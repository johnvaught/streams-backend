from django.urls import path
from .views import \
    follow_stream, \
    follow_account, \
    get_accounts_following_stream, \
    get_accounts_followed_by_stream,  \
    get_accounts_following_account, \
    get_accounts_followed_by_account

urlpatterns = [
    path('stream/<int:stream_id>/', follow_stream, name='follow_stream'),
    path('account/', follow_account, name='follow_account'),
    path('accounts/following/stream:<int:stream_id>/',
         get_accounts_following_stream, name='get_accounts_following_stream'),
    path('accounts/followedBy/stream:<int:stream_id>/',
         get_accounts_followed_by_stream, name='get_accounts_followed_by_stream'),
    path('accounts/following/handle:<str:handle>/',
         get_accounts_following_account, name='get_accounts_following_account'),
    path('accounts/followedBy/handle:<str:handle>/',
         get_accounts_followed_by_account, name='get_accounts_followed_by_account'),
]

