from django.contrib import admin

from .models import FBR, RegisterUser

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id','first_name','last_name', 'email']

admin.site.register(RegisterUser)

@admin.register(FBR)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','user','title']