from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'bio')
admin.site.register(models.User, UserAdmin)
