from django.contrib import admin
from .models import Stream


class StreamAdmin(admin.ModelAdmin):
    model = Stream


admin.site.register(Stream, StreamAdmin)
