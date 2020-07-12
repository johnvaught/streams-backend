from django.urls import path
from .views import \
    update_profile, \
    read_public_profile

app_name = 'profiles'
urlpatterns = [
    path('update/', update_profile, name='update_profile'),
    path('public/<str:handle>/', read_public_profile, name='read_public_profile'),
]
