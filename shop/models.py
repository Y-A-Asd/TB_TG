from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
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
        description=models.CharField(_("Description"), max_length=500)
    )

    class Meta:
        verbose_name = _("Feature")
        verbose_name_plural = _("Features")


class FeatureValue(TranslatableModel, BaseModel):
    translations: TranslatedFields = TranslatedFields(
        value=models.CharField(_('Title'), max_length=255),
        description=models.CharField(_("Description"), max_length=500)
    )
    parent_feature = models.ForeignKey(MainFeature, on_delete=models.CASCADE, related_name='values',
                                       verbose_name=_("Feature Values"))

    class Meta:
        verbose_name = _("Value")
        verbose_name_plural = _("Values")


class Promotion(TranslatableModel, BaseModel):
    translations: TranslatedFields = TranslatedFields(
        title=models.CharField(_('Title'), max_length=255),
        description=models.CharField(_("Description"), max_length=500)
    )

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")

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

    main_feature = models.ForeignKey(MainFeature, on_delete=models.PROTECT, related_name='collections',
                                     verbose_name='Features', null=True)

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
        slug=models.SlugField(_("Slug")),
        description=models.TextField(_("Description"), null=True, blank=True)
    )

    unit_price = models.DecimalField(_("Unit Price"), max_digits=15, decimal_places=2,
                                     validators=[MinValueValidator(1)])
    inventory = models.IntegerField(_("Inventory"), validators=[MinValueValidator(0)])
    min_inventory = models.IntegerField(_("Minimum Inventory"), validators=[MinValueValidator(0)], null=True,
                                        blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, verbose_name=_("Collection"),
                                   related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True, verbose_name=_("Promotions"), related_name='products')

    def __str__(self):
        default_language = get_language() or 'en'
        title_translation = self.translations.get(language_code=default_language)
        title = title_translation.title if title_translation else f"Product {self.pk}"
        return f'Product {self.pk} - {title}'

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

    first_name = models.CharField(_("First Name"), max_length=255),
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


class Address(BaseModel):
    zip_code = models.CharField(_("Zip Code"), max_length=10)
    path = models.CharField(_("Path"), max_length=1025)
    city = models.CharField(_("City"), max_length=255)
    province = models.CharField(_("Province"), max_length=32)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"))

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


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
    first_name = models.CharField(_("First Name"), max_length=255),
    last_name = models.CharField(_("Last Name"), max_length=255)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name=_("Order"), related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Product"), related_name='orderitems')
    unit_price = models.DecimalField(_("Unit Price"), max_digits=15, decimal_places=2,
                                     validators=[MinValueValidator(1)])
    quantity = models.PositiveSmallIntegerField(_("Quantity"))

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")


class Cart(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_("Cart"), related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    quantity = models.PositiveSmallIntegerField(_("Quantity"))

    class Meta:
        unique_together = [['cart', 'product']]
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")


class Review(BaseModel):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(_('Rating'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    name = models.CharField(max_length=255)
    description = models.TextField()
    parent_review = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    active = models.BooleanField(_("Active"), default=False)

    def __str__(self):
        return f"{self.user} - {self.name}"

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class DiscountItemManager(models.Manager):
    def get_discount(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return DiscountItems.objects \
            .select_related('discount') \
            .filter(content_type=content_type, object_id=obj_id)


class BaseDiscount(BaseModel):
    class Mode(models.TextChoices):
        DirectPrice = 'DO', _('DirectPrice')
        DiscountOff = 'DP', _('DiscountOff')

    discount = models.DecimalField(_("Discount"), max_digits=12, decimal_places=2)
    active = models.BooleanField(_("Active"), default=True)
    code = models.CharField(_('Code'), max_length=50, unique=True, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    mode = models.CharField(_('Mode'),
                            max_length=2,
                            choices=Mode,
                            default=Mode.DiscountOff)

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def __str__(self):
        return f'DISCOUNT {self.pk} - {self.discount}, {self.mode}, {self.code}'


class DiscountItems(models.Model):
    discount = models.ForeignKey(BaseDiscount, on_delete=models.PROTECT, verbose_name=_("Discount"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=33)
    content_object = GenericForeignKey()
    objects = DiscountItemManager()

    class Meta:
        """https://docs.djangoproject.com/en/5.0/ref/models/constraints/#uniqueconstraint"""
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['content_type', 'object_id'],
        #         condition=models.Q(discount__active=True),
        #         name='unique_active_discount'
        #     )
        # ]
        verbose_name = _("Discount Item")
        verbose_name_plural = _("Discount Items")

    def clean(self):
        existing_discount_item = DiscountItems.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
            discount__active=True
        ).exclude(pk=self.pk)

        if existing_discount_item.exists():
            raise ValidationError(_('There is already an active discount for this item.'))


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
    receipt_number = models.CharField(_("Receipt Number"), max_length=255)

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
