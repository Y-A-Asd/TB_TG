from django.db.models import F
from django import forms
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Count, Sum
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from dal import autocomplete
from parler.admin import TranslatableAdmin, TranslatableTabularInline
from tags.models import TaggedItem
from . import models
from .models import CartItem, Cart, Review, BaseDiscount, DiscountItems, Transaction, Address, FeatureValue, \
    MainFeature, Order, OrderItem, SiteSettings


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    verbose_name = _('Tag')
    verbose_name_plural = _('Tags')


class FeatureValueInline(TranslatableTabularInline):
    model = FeatureValue
    extra = 1
    exclude = ['deleted_at', 'created_at', 'updated_at']


@admin.register(MainFeature)
class MainFeatureAdmin(TranslatableAdmin):
    inlines = [FeatureValueInline]
    list_display = ['title', 'description']
    search_fields = ['title']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    class Meta:
        model = MainFeature


@admin.register(FeatureValue)
class FeatureValueAdmin(TranslatableAdmin):
    list_display = ['value', 'description', 'parent_feature']
    search_fields = ['value']
    list_filter = ['parent_feature']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    class Meta:
        model = FeatureValue


class InventoryFilter(admin.SimpleListFilter):
    title = _('Inventory')
    parameter_name = 'inventory'
    exclude = ['deleted_at', 'created_at', 'updated_at']
    inlines = [TagInline]

    def lookups(self, request, model_admin):
        return [
            ('<min', _('Low')),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<min':
            return queryset.filter(inventory__lt=F('min_inventory'))


@admin.register(models.Promotion)
class PromotionAdmin(TranslatableAdmin):
    exclude = ['deleted_at', 'created_at', 'updated_at']
    list_display = ('title', 'description')
    inlines = [TagInline]


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']
    inlines = [TagInline]
    exclude = ['deleted_at', 'created_at', 'updated_at']

    def thumbnail(self, obj):
        if obj.image.name != '':
            return format_html(
                f'<img class="thumbnail" src="{obj.image.url}"/>'
            )


@admin.register(models.Product)
class ProductAdmin(TranslatableAdmin):
    autocomplete_fields = ['collection']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}

    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title', 'min_inventory']
    list_editable = ['unit_price']
    list_filter = ['collection', 'updated_at', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']
    exclude = ['deleted_at', 'created_at', 'updated_at']
    inlines = [TagInline, ProductImageInline]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory <= product.min_inventory:
            return _('Low')
        return _('OK')

    @admin.action(description=_('Clear inventory'))
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            _('{count} products were successfully updated.').format(count=updated_count),
            messages.ERROR
        )

    class Media:
        css = {
            'all': ['shop/style.css']
        }


@admin.register(models.Collection)
class CollectionAdmin(TranslatableAdmin):
    autocomplete_fields = ['parent', 'main_feature']
    list_display = ['title', 'products_count', 'main_feature', 'parent']
    search_fields = ['title']
    exclude = ['deleted_at', 'created_at', 'updated_at']
    inlines = [TagInline]

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
                reverse('admin:shop_product_changelist')
                + '?'
                + urlencode({'collection__id': str(collection.id)}))
        return format_html('<a href="{}">{} {}</a>', url, collection.products_count, _('Products'))

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    exclude = ['deleted_at', 'created_at', 'updated_at']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    exclude = ['deleted_at', 'created_at', 'updated_at']
    inlines = [TagInline, AddressInline]

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
                reverse('admin:shop_order_changelist')
                + '?'
                + urlencode({'customer__id': str(customer.id)}))
        return format_html('<a href="{}">{} {}</a>', url, customer.orders_count, _('Orders'))

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    exclude = ['deleted_at', 'created_at', 'updated_at']
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 20
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ['deleted_at', 'updated_at']
    autocomplete_fields = ['customer']
    list_filter = ['customer', 'order_status']
    inlines = [OrderItemInline]
    list_display = ['id', 'customer', 'order_status', 'total_price', 'view_order_items', 'created_at']
    search_fields = ['id', 'customer__user__username']
    actions = ['mark_as_delivered']

    def total_price(self, obj):
        return obj.orders.aggregate(total_price=Sum(F('unit_price') * F('quantity')))['total_price']

    total_price.short_description = _("Total Price")

    def mark_as_delivered(self, request, queryset):
        queryset.update(order_status=Order.OrderStatus.ORDER_STATUS_DELIVERED)

    mark_as_delivered.short_description = _("Mark selected orders as delivered")

    def view_order_items(self, obj):
        order_items_url = reverse('admin:shop_orderitem_changelist') + f'?order__id__exact={obj.id}'
        return format_html('<a href="{}">View Order Items</a>', order_items_url)

    view_order_items.short_description = _('Order Items')

    list_display_links = ['id', 'created_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'unit_price', 'quantity']
    list_filter = ['order', 'product']
    search_fields = ['order__id', 'product__title']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        return ['order', 'product']

    def get_total_price(self, obj):
        return obj.unit_price * obj.quantity

    get_total_price.short_description = _("Total Price")


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    exclude = ['deleted_at', 'created_at', 'updated_at']


class CartItemAdminForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.cleaned_data.get('product')

        if product and quantity > product.inventory:
            raise ValidationError(_("Quantity cannot be greater than the available inventory."))

        return quantity


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    form = CartItemAdminForm
    list_display = ['cart', 'product', 'quantity', 'view_cart']
    list_filter = ['cart', 'product']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    def view_cart(self, obj):
        cart_url = reverse('admin:shop_cart_change', args=[obj.cart.id])
        return format_html('<a href="{}">View Cart Items</a>', cart_url)

    def save_model(self, request, obj, form, change):
        if obj.product and obj.quantity > obj.product.inventory:
            raise ValidationError(_("Quantity cannot be greater than the available inventory."))

        super().save_model(request, obj, form, change)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'view_cart_items']
    readonly_fields = ['view_cart_items']
    inlines = [CartItemInline]
    exclude = ['deleted_at', 'created_at', 'updated_at']

    def view_cart_items(self, obj):
        cart_items_url = reverse('admin:shop_cartitem_changelist') + f'?cart__id__exact={obj.id}'
        return format_html('<a href="{}">View Cart Items</a>', cart_items_url)

    view_cart_items.short_description = 'Cart Items'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'title', 'parent_review', 'rating']
    list_filter = ['user', 'product']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    exclude = ['deleted_at', 'updated_at']


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
        if mode == BaseDiscount.Mode.DirectPrice and discount < 101:
            raise ValidationError({'discount': _('Invalid discount!(Check Mode again)')})

        if mode == BaseDiscount.Mode.DiscountOff and discount > 99:
            raise ValidationError({'discount': _('Invalid discount(Check Mode again)')})

        return cleaned_data


class DiscountItemsInline(admin.TabularInline):
    model = DiscountItems
    extra = 1


@admin.register(BaseDiscount)
class BaseDiscountAdmin(admin.ModelAdmin):
    form = BaseDiscountAdminForm
    list_filter = ['mode', 'active', 'valid_from', 'valid_to']
    search_fields = ['code']
    date_hierarchy = 'valid_from'
    inlines = [DiscountItemsInline]


@admin.register(DiscountItems)
class DiscountItemsAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'discount', 'get_content_object_link']
    list_filter = ['content_type', 'discount__mode', 'discount__active']
    search_fields = ['object_id']
    readonly_fields = ['get_content_object_link']
    exclude = ['content_object']

    def get_content_object_link(self, obj):
        link = reverse('admin:%s_%s_change' % (obj.content_type.app_label, obj.content_type.model),
                       args=[obj.object_id])
        return format_html('<a href="{}">{}</a>', link, obj.content_object)

    get_content_object_link.short_description = _('Content Object')


"""
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
https://stackoverflow.com/questions/43852601/offering-choices-that-depend-on-other-fields-in-django-admin
"""


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['order_link', 'payment_status', 'total_price', 'customer', 'receipt_number']
    list_filter = ['payment_status', 'customer']
    search_fields = ['order__id', 'customer__user__username', 'receipt_number']
    actions = ['mark_as_complete']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    def order_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse('admin:shop_order_change', args=[obj.order.id]), obj.order)

    order_link.short_description = _('Order')

    def mark_as_complete(self, request, queryset):
        queryset.update(payment_status=Transaction.PaymentStatus.PAYMENT_STATUS_COMPLETE)

    mark_as_complete.short_description = _('Mark selected transactions as complete')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.payment_status == Transaction.PaymentStatus.PAYMENT_STATUS_COMPLETE:
            return self.readonly_fields + ('order', 'payment_status', 'total_price', 'customer', 'receipt_number')
        return self.readonly_fields


class SiteSettingsAdmin(TranslatableAdmin):
    list_display = ['id', 'phone_number', 'logo_thumbnail']
    readonly_fields = ['logo_thumbnail']
    fieldsets = [
        (_('General Settings'), {'fields': ['phone_number', 'social_media_links']}),
        (_('Translations'), {'fields': ['footer_text', 'address']}),
        (_('Logo'), {'fields': ['logo', 'logo_thumbnail']}),
    ]

    def logo_thumbnail(self, obj):
        if obj.logo:
            return '<img src="{}" style="max-height: 100px; max-width: 150px;"/>'.format(obj.logo.url)
        return _('No Image')

    logo_thumbnail.allow_tags = True
    logo_thumbnail.short_description = _('Logo Preview')


admin.site.register(SiteSettings, SiteSettingsAdmin)
