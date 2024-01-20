from django.contrib.auth.models import Permission

from .models import User
from shop.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from shop.admin import ProductAdmin
from tags.models import TaggedItem
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    verbose_name = _('Tag')
    verbose_name_plural = _('Tags')


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ['codename']
    pass


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
