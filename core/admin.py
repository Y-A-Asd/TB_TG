from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey
from django.shortcuts import get_object_or_404
from .models import User, AuditLog
from shop.models import Product
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from shop.admin import TagInline
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


@admin.register(AuditLog)  # pragma: no cover
class AuditlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'timestamp', 'changes', 'table_name')
    actions = ['revert']

    @admin.action(description=_('Action Revert'))
    def revert(self, request, queryset):
        if queryset.count() != 1:
            messages.error(request, _("Please select only one row to revert."))
            return

        log_entry = queryset.first()
        after_log = AuditLog.objects.all().filter(row_id=log_entry.row_id, timestamp__gte=log_entry.timestamp)

        app_name, model_name = log_entry.table_name.split('_', 1)
        model_name: str = model_name.replace("_", "")
        # mage mishe inghadar ziba bashe ?? :-)

        model_class = apps.get_model(app_label=app_name, model_name=model_name)

        model_instance = get_object_or_404(model_class, id=log_entry.row_id)
        changes = {}
        for log in after_log:

            if log.changes:
                for field_name, field_data in log.changes.items():

                    if isinstance(model_instance._meta.get_field(field_name), ForeignKey):
                        field_data['old_value'] = model_instance._meta.get_field(field_name).related_model.objects.get(
                            pk=(field_data['old_value']))

                    setattr(model_instance, field_name, field_data['old_value'])
                    try:
                        if model_instance.deleted_at == "None":
                            model_instance.deleted_at = None
                    except AttributeError:
                        pass

                model_instance.save()
                changes[field_name] = str(field_data)

        self.message_user(request, _("Changes reverted successfully."), messages.SUCCESS)
