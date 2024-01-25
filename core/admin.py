from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import User
from shop.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from shop.admin import ProductAdmin, ProductImageInline, TagInline
from tags.models import TaggedItem
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ['app_label', 'model']
    search_fields = ['app_label', 'model']
    inlines = [TagInline]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ['codename']
    inlines = [TagInline]


class PermissionInline(admin.TabularInline):
    autocomplete_fields = ['permission']
    model = User.user_permissions.through
    extra = 1


class GroupInline(admin.TabularInline):
    autocomplete_fields = ['group']
    model = User.groups.through
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # admin.site.unregister(User)
    list_display = ('phone_number', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login')
    readonly_fields = ('last_login', 'phone_number', 'email')

    fieldsets = (
        (None, {'fields': ['phone_number', 'email']}),
        ('Permissions', {'fields': ['is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions']}),
        ('Last_login', {'fields': ['last_login', ]}),
    )

    add_fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ['phone_number', 'email', ],
        }),
    )

    search_fields = ('phone_number', 'email')
    ordering = ('phone_number', 'email')
    filter_horizontal = ('groups', 'user_permissions')

    inlines = [PermissionInline, GroupInline]
