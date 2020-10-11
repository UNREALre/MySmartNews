from django.contrib import admin

from user.models import UserSource


class UserSourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserSource, UserSourceAdmin)
