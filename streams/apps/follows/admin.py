from django.contrib import admin
from .models import ProfileFollow, StreamFollow


class ProfileFollowAdmin(admin.ModelAdmin):
    model = ProfileFollow


class StreamFollowAdmin(admin.ModelAdmin):
    model = StreamFollow


admin.site.register(ProfileFollow, ProfileFollowAdmin)
admin.site.register(StreamFollow, StreamFollowAdmin)
