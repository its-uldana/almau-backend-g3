from django.contrib import admin
from .models import User, ResetPassword


# Register your models here.

class ResetClassAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at',)


admin.site.register(User)
admin.site.register(ResetPassword, ResetClassAdmin)
