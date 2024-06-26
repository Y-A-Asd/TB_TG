from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator
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
    """
    Base model containing common fields and functionality for other models.

    Attributes:
        created_at (DateTimeField): The datetime when the object was created.
        updated_at (DateTimeField): The datetime when the object was last updated.
        deleted_at (DateTimeField, optional): The datetime when the object was soft-deleted.

    Methods:
        delete(): Soft deletes the object by setting the 'deleted_at' field.
    """
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
    """
    Model to record changes made to other models in the system.

    Attributes:
        user (ForeignKey): The user who performed the action.
        action (CharField): The type of action performed (CREATE, UPDATE, DELETE).
        timestamp (DateTimeField): The datetime when the action was performed.
        table_name (CharField): The name of the table/model being modified.
        row_id (TextField, optional): The ID of the modified row.
        old_value (JSONField, optional): The previous value of the modified row.
        changes (JSONField, optional): The changes made to the row.
    """
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


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError(_('The phone number or email field must be set'))
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user in the system.

    Attributes:
        phone_number (CharField): The user's phone number.
        email (EmailField): The user's email address.
        password (CharField): The user's password (hashed).
        is_active (BooleanField): Indicates whether the user is active.
        is_staff (BooleanField): Indicates whether the user is a staff member.
        last_login (DateTimeField): The datetime when the user last logged in.
    """
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message=_('Phone number must start with "09" and have 11 digits.'),
                code='invalid_phone_number'
            )
        ],
        verbose_name=_("Phone Number")
    )

    email = models.EmailField(unique=True, verbose_name=_("Email"))
    password = models.CharField(max_length=128, verbose_name=_("Password"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Staff"))
    last_login = models.DateTimeField(auto_now_add=True, verbose_name=_('Last Login'))

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")