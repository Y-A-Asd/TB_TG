from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from .models import Tag, TaggedItem
from django.utils.translation import gettext_lazy as _


# Register your models here.


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 1
    verbose_name_plural = _("Tags")
    autocomplete_fields = ['tag']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['label']
    search_fields = ['label']


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['tag', 'content_type', 'object_id']
    list_filter = ['tag', 'content_type']
    search_fields = ['tag__label']
    ordering = ['-id']
    autocomplete_fields = ['tag']
