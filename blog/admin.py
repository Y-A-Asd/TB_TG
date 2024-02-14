from django.contrib import admin
from django.utils.html import format_html
from parler.admin import TranslatableAdmin
from .models import Blog, BlogComment


# Register your models here.
@admin.register(Blog)
class BlogAdmin(TranslatableAdmin):
    list_filter = ['author', 'updated_at']
    search_fields = ('title', 'body')
    list_display = ['id', 'title', 'body', 'thumbnail', 'views', 'author']
    readonly_fields = ('id', 'views')
    exclude = ['deleted_at']
    date_hierarchy = 'updated_at'
    list_select_related = ['author']

    def thumbnail(self, obj):
        if obj.image.name != '':
            return format_html(
                f'<img class="thumbnail" src="{obj.image.url}"/>'
            )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'blog', 'subject', 'message', 'active']
    list_filter = ['customer', 'blog']
    search_fields = ['subject', 'message']
    exclude = ['deleted_at']
    date_hierarchy = 'updated_at'
