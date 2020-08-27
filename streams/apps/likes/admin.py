from django.contrib import admin
from .models import PostLike


class PostLikeAdmin(admin.ModelAdmin):
    model = PostLike


admin.site.register(PostLike, PostLikeAdmin)
