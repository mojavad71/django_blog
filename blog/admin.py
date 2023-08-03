from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datetime_create', 'status',)
    ordering = ('-status',)


# admin.site.register(Post, PostAdmin)

