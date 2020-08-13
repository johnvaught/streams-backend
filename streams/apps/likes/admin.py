from django.contrib import admin
from .models import Like


class LikeAdmin(admin.ModelAdmin):
    model = Like


admin.site.register(Like, LikeAdmin)
