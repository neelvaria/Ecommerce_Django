from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'bio')
admin.site.register(User, UserAdmin)

class contactadmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'message','phone','date')
admin.site.register(contactus,contactadmin)

class profile_details_admin(admin.ModelAdmin):
    list_display = ('user','full_name', 'bio', 'phone', 'verified', 'image')
admin.site.register(profile_details,profile_details_admin)

