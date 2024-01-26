from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel


class UsageCount(models.Model):
    discount = models.ForeignKey('BaseDiscount', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def increment(self):
        self.count += 1
        self.save()

    def __str__(self):
        return f"UsageCount for {self.discount.code}: {self.count}"


class BaseDiscount(BaseModel):
    class Mode(models.TextChoices):
        DirectPrice = 'DO', _('Direct Price')
        DiscountOff = 'DP', _('Discount Off')
        PersonCode = 'PC', _('One Time Use')
        EventCode = 'EC', _('Multy Time Use')

    discount = models.DecimalField(_("Discount"), max_digits=12, decimal_places=2)
    active = models.BooleanField(_("Active"), default=True)
    code = models.CharField(_('Code'), max_length=50, unique=True, null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    mode = models.CharField(_('Mode'),
                            max_length=2,
                            choices=Mode,
                            default=Mode.DiscountOff)

    def ensure_availability(self):
        now = timezone.now()
        if self.valid_to and self.valid_to < now:
            self.active = False
            # self.save()
            return False
        if self.valid_from and self.valid_from > now:
            self.active = False
            # self.save()
            return False
        if self.code and self.mode == self.Mode.PersonCode and self.used:
            self.active = False
            # self.save()
            return False
        return True

    def clean(self):
        if self.code and not (self.valid_from and self.valid_to):
            raise ValidationError({
                'code': _("Code-based discounts must have valid_from and valid_to dates.")
            })

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def __str__(self):
        return f'DISCOUNT {self.pk} - {self.discount}, {self.mode}, {self.code}'


