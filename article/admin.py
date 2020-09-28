from django.contrib import admin

from .models import Source, Category


class SourceAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Source, SourceAdmin)
admin.site.register(Category, CategoryAdmin)
