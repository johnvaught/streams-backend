from django.urls import path
from .views import \
    create_account, \
    read_account, \
    update_account, \
    delete_account


app_name = 'accounts'
urlpatterns = [
    path('create/', create_account, name='create_account'),
    path('read/', read_account, name='read_account'),
    path('update/', update_account, name='update_account'),
    path('delete/', delete_account, name='delete_account'),
]
