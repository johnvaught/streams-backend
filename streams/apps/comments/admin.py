from django.contrib import admin
from .models import PostComment


class PostCommentAdmin(admin.ModelAdmin):
    model = PostComment


admin.site.register(PostComment, PostCommentAdmin)
