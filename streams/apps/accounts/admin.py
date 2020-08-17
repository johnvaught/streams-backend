from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ['id', 'handle']


admin.site.register(Account, AccountAdmin)
