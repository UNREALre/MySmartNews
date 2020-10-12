from django.contrib import admin

from user.models import UserSources


class UserSourcesAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserSources, UserSourcesAdmin)
