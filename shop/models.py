from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum, F
from discount.models import BaseDiscount
from shop.validator import validate_file_size
from django.utils.translation import gettext_lazy as _, get_language
from django.db import models
from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields
from core.models import BaseModel
import uuid


class MainFeature(TranslatableModel, BaseModel):
    translations: TranslatedFields = TranslatedFields(
        title=models.CharField(_('Title'), max_length=255),
        description=models.CharField(_("Description"), max_length=500),
        value=models.CharField(_('Value'), max_length=255),
    )

    class Meta:
        verbose_name = _("Feature")
        verbose_name_plural = _("Features")


class Promotion(TranslatableModel, BaseModel):
    translations: TranslatedFields = TranslatedFields(
        title=models.CharField(_('Title'), max_length=255),
        description=models.CharField(_("Description"), max_length=500, null=True, blank=True)
    )

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")

    # def clean(self):
    #     existing_discount_item = self.discount.objects.filter(
    #         content_type=self.content_type,
    #         object_id=self.object_id,
    #         discount__active=True
    #     ).exclude(pk=self.pk)
    #
    #     if existing_discount_item.exists():
    #         raise ValidationError(_('There is already an active discount for this item.'))

    def __str__(self):
        default_language = get_language() or 'en'
        description_translation = self.translations.get(language_code=default_language)
        description = description_translation.description if description_translation else f"Promotion {self.pk}"
        return f'Promotion {self.pk} - {description}'


class Collection(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=255)
    )

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcollection',
                               verbose_name=_("Parent"))

    @property
    def is_subcollection(self):
        return self.parent is not None

    def __str__(self):
        default_language = get_language() or 'en'
        title_translation = self.translations.get(language_code=default_language)
        title = title_translation.title if title_translation else f"Collection {self.pk}"
        return f'Collection {self.pk} - {title}'

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")
        ordering = ["translations__title"]


class Product(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(_("Title"), max_length=255),
        slug=models.SlugField(_("Slug"), null=True, blank=True),
        description=models.TextField(_("Description"), null=True, blank=True)
    )

    unit_price = models.DecimalField(_("Unit Price"), max_digits=15, decimal_places=2,
                                     validators=[MinValueValidator(1)])
    inventory = models.IntegerField(_("Inventory"), validators=[MinValueValidator(0)])
    min_inventory = models.IntegerField(_("Minimum Inventory"), validators=[MinValueValidator(0)],
                                        null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, verbose_name=_("Collection"),
                                   related_name='products', null=True, blank=True)
    promotions = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name=_("Promotions"),
                                   related_name='products')
    discount = models.ForeignKey(BaseDiscount, on_delete=models.CASCADE, verbose_name=_("Discount"),
                                 null=True, blank=True)

    value_feature = models.ManyToManyField(MainFeature, related_name='value_features',
                                           verbose_name='Features', blank=True)

    def __str__(self):
        default_language = get_language() or 'en'
        title_translation = self.translations.get(language_code=default_language)
        title = title_translation.title if title_translation else f"Product {self.pk}"
        return f'Product {self.pk} - {title} - {self.unit_price}'

    @property
    def price_after_off(self, ):
        if self.discount:
            self.discount.ensure_availability()
            if self.discount.mode == self.discount.Mode.DirectPrice:
                return self.unit_price - self.discount.discount
            elif self.discount.mode == self.discount.Mode.DiscountOff:
                return self.unit_price - (self.unit_price * self.discount.discount / 100)
            else:
                raise ValueError(f"Invalid discount mode: {self.discount.mode}")
        return self.unit_price

        # def clean(self):
        #     existing_discount_item = self.discount.objects.filter(
        #         content_type=self.content_type,
        #         object_id=self.object_id,
        #         discount__active=True
        #     ).exclude(pk=self.pk)

        if existing_discount_item.exists():
            raise ValidationError(_('There is already an active discount for this item.'))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["translations__title"]


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
        # ordering = ["first_name", "last_name"]
        permissions = [
            ('view_history', 'Can view history')
        ]


class Cart(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"))


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_("Cart"), related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    # unit_price = models.DecimalField(_('Price'),max_digits=15, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(_("Quantity"))

    class Meta:
        unique_together = [['cart', 'product']]
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")


class Address(BaseModel):
    zip_code = models.CharField(_("Zip Code"), max_length=10)
    path = models.CharField(_("Path"), max_length=1025)
    city = models.CharField(_("City"), max_length=255)
    province = models.CharField(_("Province"), max_length=32)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"))
    default = models.BooleanField(_("Default"), default=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def save(self, *args, **kwargs):
        if self.default:
            Address.objects.filter(customer=self.customer).exclude(id=self.id).update(default=False)

        super().save(*args, **kwargs)


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        ORDER_STATUS_NOT_PAID = 'N', _('Not Paid')
        ORDER_STATUS_PENDING = 'P', _('Pending')
        ORDER_STATUS_SHIPPING = 'S', _('Shipping')
        ORDER_STATUS_DELIVERED = 'D', _('Delivered')
        ORDER_STATUS_FAILED = 'F', _('Failed')

    order_status = models.CharField(_("Payment Status"), max_length=1, choices=OrderStatus,
                                    default=OrderStatus.ORDER_STATUS_NOT_PAID)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"))
    zip_code = models.CharField(_("Zip Code"), max_length=10)
    path = models.CharField(_("Path"), max_length=1025)
    city = models.CharField(_("City"), max_length=255)
    province = models.CharField(_("Province"), max_length=32)
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def get_total_price(self):
        total_price = self.orders.aggregate(total_price=Sum(F('unit_price') * F('quantity')))['total_price']
        return total_price if total_price is not None else 0


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name=_("Order"), related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Product"), related_name='orderitems')
    unit_price = models.DecimalField(_("Unit Price"), max_digits=15, decimal_places=2,
                                     validators=[MinValueValidator(1)])
    quantity = models.PositiveSmallIntegerField(_("Quantity"))

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")


class Review(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Product')
    rating = models.PositiveIntegerField(_('Rating'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField()
    parent_review = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
                                      verbose_name='Reply to')
    active = models.BooleanField(_("Active"), default=False)

    def __str__(self):
        return f"{self.customer} - {self.title}"

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class Transaction(BaseModel):
    class PaymentStatus(models.TextChoices):
        PAYMENT_STATUS_PENDING = 'P', _('Pending')
        PAYMENT_STATUS_COMPLETE = 'C', _('Complete')
        PAYMENT_STATUS_FAILED = 'F', _('Failed')

    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name=_("Order"), related_name='transaction')
    payment_status = models.CharField(_("Payment Status"), max_length=1, choices=PaymentStatus,
                                      default=PaymentStatus.PAYMENT_STATUS_PENDING)
    total_price = models.DecimalField(_("Total Price"), max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"))
    receipt_number = models.CharField(_("Receipt Number"), max_length=255, null=True)

    def __str__(self):
        return f"Transaction for Order #{self.order.pk} - {self.get_payment_status_display()}"

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")


class SiteSettings(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        footer_text=models.TextField(_("Footer Text"), blank=True, null=True),
        address=models.TextField(_("Address"), blank=True, null=True)
    )
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True, null=True)
    logo = models.ImageField(_("Logo"), upload_to='site_settings/logos/', blank=True, null=True)
    social_media_links = models.JSONField(_("Social Media Links"), blank=True, null=True)

    def __str__(self):
        return f"Site Settings {self.pk}"

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

# class WishList(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"))
#
#     class Meta:
#         verbose_name = 'WishList'
#         verbose_name_plural = 'WishList'
#
#     def __str__(self):
#         return f'{self.customer.first_name} {self.customer.last_name}'
