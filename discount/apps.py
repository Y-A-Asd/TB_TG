from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DiscountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'discount'
    verbose_name = _('Discount')
