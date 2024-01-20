from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # Exclude soft-deleted items by default
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    deleted_at = models.DateTimeField(_("Deleted at"), null=True, blank=True)

    defman = models.Manager()
    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None,
                             verbose_name=_("User"))
    action = models.CharField(_("Action"), max_length=10)  # 'CREATE', 'UPDATE', 'DELETE'
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    table_name = models.CharField(_("Table Name"), max_length=50)
    row_id = models.TextField(_("Row ID"), null=True, blank=True)
    old_value = models.JSONField(_("Old Value"), null=True)
    changes = models.JSONField(_("Changes"), null=True)

    class Meta:
        verbose_name = _("Audit Log")
        verbose_name_plural = _("Audit Logs")


