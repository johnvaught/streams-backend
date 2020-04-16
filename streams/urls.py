from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # The admin site.
    path('admin/', admin.site.urls),
    # Tokens API
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Streams apps
    path('accounts/', include('streams.apps.accounts.urls')),
    path('profiles/', include('streams.apps.profiles.urls')),
    path('posts/', include('streams.apps.posts.urls')),
    path('streams/', include('streams.apps.streams.urls')),
    path('follows/', include('streams.apps.follows.urls')),
]
