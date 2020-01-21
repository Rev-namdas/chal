from django.contrib import admin
from login.models import loginModel, AdminPassword
# Register your models here.

class loginModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'time')


class adminPasswordAdmin(admin.ModelAdmin):
    list_display = ['admin_password']


admin.site.register(loginModel, loginModelAdmin)

admin.site.register(AdminPassword, adminPasswordAdmin)