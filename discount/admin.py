from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from discount.models import BaseDiscount


class BaseDiscountAdminForm(forms.ModelForm):
    class Meta:
        model = BaseDiscount
        fields = ['code', 'discount', 'mode', 'active', 'valid_from', 'valid_to']

    def clean(self):
        """
            https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
            https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/#overriding-clean-on-a-modelformset
            https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/#overriding-methods-on-an-inlineformset
        """
        cleaned_data = super().clean()
        mode = cleaned_data.get('mode')
        discount = cleaned_data.get('discount')
        active = cleaned_data.get('active')
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')
        base = BaseDiscount(mode=mode, discount=discount, active=active, valid_to=valid_to, valid_from=valid_from)
        if mode == BaseDiscount.Mode.DirectPrice and discount < 101:
            raise ValidationError({'discount': _('Invalid discount!(Check Mode again)')})

        if mode == BaseDiscount.Mode.DiscountOff and discount > 99:
            raise ValidationError({'discount': _('Invalid discount(Check Mode again)')})

        if not base.ensure_availability() and BaseDiscount.active:
            raise ValidationError({'discount': _('Invalid discount(Check Dates again)')})
        return cleaned_data


# class DiscountItemsInline(admin.TabularInline):
#     model = DiscountItems
#     extra = 1


@admin.register(BaseDiscount)
class BaseDiscountAdmin(admin.ModelAdmin):
    form = BaseDiscountAdminForm
    list_filter = ['mode', 'active', 'valid_from', 'valid_to']
    search_fields = ['code']
    date_hierarchy = 'valid_from'

# @admin.register(DiscountItems)
# class DiscountItemsAdmin(admin.ModelAdmin):
#     list_display = ['content_type', 'object_id', 'discount', 'get_content_object_link']
#     list_filter = ['content_type', 'discount__mode', 'discount__active']
#     search_fields = ['object_id']
#     readonly_fields = ['get_content_object_link']
#     exclude = ['content_object']
#
#     def get_content_object_link(self, obj):
#         link = reverse('admin:%s_%s_change' % (obj.content_type.app_label, obj.content_type.model),
#                        args=[obj.object_id])
#         return format_html('<a href="{}">{}</a>', link, obj.content_object)
#
#     get_content_object_link.short_description = _('Content Object')
