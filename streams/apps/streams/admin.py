from django.contrib import admin
from .models import Stream


class StreamAdmin(admin.ModelAdmin):
    model = Stream
    list_display = ['id', 'owner', 'name', 'is_private']


admin.site.register(Stream, StreamAdmin)
