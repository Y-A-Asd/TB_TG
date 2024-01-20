from django.contrib import admin
from .models import Tag
from django.utils.translation import gettext_lazy as _


# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = [_('label')]
