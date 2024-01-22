from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from core.models import BaseModel
import uuid


class Promotion(BaseModel):
    description = models.CharField(_("Description"), max_length=255)
    discount = models.FloatField(_("Discount"))

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")


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
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"))
    description = models.TextField(_("Description"), null=True, blank=True)
    unit_price = models.DecimalField(_("Unit Price"), max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField(_("Inventory"), validators=[MinValueValidator(0)])
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, verbose_name=_("Collection"),
                                   related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True, verbose_name=_("Promotions"))

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["title"]


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


class Order(BaseModel):
    class PaymentStatus(models.TextChoices):
        PAYMENT_STATUS_PENDING = 'P', _('Pending')
        PAYMENT_STATUS_COMPLETE = 'C', _('Complete')
        PAYMENT_STATUS_FAILED = 'F', _('Failed')

    placed_at = models.DateTimeField(_("Placed At"), auto_now_add=True)
    payment_status = models.CharField(_("Payment Status"), max_length=1, choices=PaymentStatus,
                                      default=PaymentStatus.PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name=_("Order"))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Product"), related_name='orderitems')
    quantity = models.PositiveSmallIntegerField(_("Quantity"))
    unit_price = models.DecimalField(_("Unit Price"), max_digits=6, decimal_places=2)

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
