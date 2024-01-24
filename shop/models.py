from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _, get_language
from django.db import models
from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields
from core.models import BaseModel
import uuid

from shop.validator import validate_file_size


class Promotion(TranslatableModel, BaseModel):
    translations: TranslatedFields = TranslatedFields(
        title=models.CharField(_('Title'), max_length=255),
        description=models.CharField(_("Description"), max_length=255)
    )

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")

    def __str__(self):
        default_language = get_language() or 'en'
        description_translation = self.translations.get(language_code=default_language)
        description = description_translation.description if description_translation else f"Promotion {self.pk}"
        return f'Promotion {self.pk} - {description}'


class Collection(BaseModel):
    title = models.CharField(_("Title"), max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcollection',
                               verbose_name=_("Parent"))

    @property
    def is_subcollection(self):
        return self.parent is not None

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")
        ordering = ["title"]


class Product(BaseModel):
    title = models.CharField(_("Title"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"))
    description = models.TextField(_("Description"), null=True, blank=True)
    unit_price = models.DecimalField(_("Unit Price"), max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField(_("Inventory"), validators=[MinValueValidator(0)])
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, verbose_name=_("Collection"),
                                   related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True, verbose_name=_("Promotions"), related_name='products')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["title"]


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='shop/images', validators=[validate_file_size])


class Customer(BaseModel):
    class MembershipStatus(models.TextChoices):
        MEMBERSHIP_BRONZE = 'B', _('Bronze')
        MEMBERSHIP_SILVER = 'S', _('Silver')
        MEMBERSHIP_GOLD = 'G', _('Gold')

    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    birth_date = models.DateField(_("Birth Date"), null=True, blank=True)
    membership = models.CharField(_("Membership"), max_length=1, choices=MembershipStatus,
                                  default=MembershipStatus.MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ["first_name", "last_name"]
        permissions = [
            ('view_history', 'Can view history')
        ]


class Order(BaseModel):
    class PaymentStatus(models.TextChoices):
        PAYMENT_STATUS_PENDING = 'P', _('Pending')
        PAYMENT_STATUS_COMPLETE = 'C', _('Complete')
        PAYMENT_STATUS_FAILED = 'F', _('Failed')

    payment_status = models.CharField(_("Payment Status"), max_length=1, choices=PaymentStatus,
                                      default=PaymentStatus.PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name=_("Order"), related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Product"), related_name='orderitems')
    quantity = models.PositiveSmallIntegerField(_("Quantity"))

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")


class Address(BaseModel):
    street = models.CharField(_("Street"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"))

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class Cart(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_("Cart"), related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    quantity = models.PositiveSmallIntegerField(_("Quantity"))

    class Meta:
        unique_together = [['cart', 'product']]
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")


class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()


class DiscountItemManager(models.Manager):
    def get_discount(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return DiscountItems.objects \
            .select_related('discount') \
            .filter(content_type=content_type, object_id=obj_id)


class BaseDiscount(BaseModel):
    discount = models.DecimalField(_("Discount"), max_digits=12, decimal_places=2)
    active = models.BooleanField(_("Active"), default=True)
    timestamp = models.DateTimeField(_("Timestamp"), default=None)

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")


class DiscountItems(models.Model):
    discount = models.ForeignKey(BaseDiscount, on_delete=models.PROTECT, verbose_name=_("Discount"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=33)
    content_object = GenericForeignKey()
    objects = DiscountItemManager()

    class Meta:
        """https://docs.djangoproject.com/en/5.0/ref/models/constraints/#uniqueconstraint"""
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id'],
                condition=models.Q(active=True),
                name='unique_active_discount'
            )
        ]
        verbose_name = _("Discount Item")
        verbose_name_plural = _("Discount Items")


