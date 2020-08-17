from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['id', 'handle', 'full_name']


admin.site.register(Profile, ProfileAdmin)
