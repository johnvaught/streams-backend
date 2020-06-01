from django.urls import path
from .views import \
    create_stream, \
    update_stream, \
    delete_stream, \
    read_public_streams_for, \
    read_stream, \
    read_public_stream

urlpatterns = [
    path('create/', create_stream, name='create_stream'),
    path('read/public/<int:stream_id>/', read_public_stream, name='read_public_stream'),
    path('read/public/<str:handle>/', read_public_streams_for, name='read_public_streams_for'),
    path('read/<int:stream_id>/', read_stream, name='read_stream'),
    path('update/<int:stream_id>/', update_stream, name='update_stream'),
    path('delete/<int:stream_id>/', delete_stream, name='delete_stream'),
]
