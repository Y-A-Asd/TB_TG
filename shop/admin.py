from django.contrib.admin import TabularInline
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
from parler.forms import TranslatableModelForm

from tags.models import TaggedItem
from . import models
from .filters import MainFeatureFilter
from .models import Review, Transaction, Address, \
    MainFeature, Order, OrderItem, SiteSettings, Product, Collection


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    verbose_name = _('Tag')
    verbose_name_plural = _('Tags')


@admin.register(MainFeature)
class MainFeatureAdmin(TranslatableAdmin):
    list_display = ['title', 'description', 'value']
    search_fields = ['title']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    class Meta:
        model = MainFeature


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


class FeatureInline(TabularInline):
    model = Product.value_feature.through
    extra = 1


class CollectionAdminForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['parent']
    list_display = ['title', 'products_count', 'parent']
    search_fields = ['title']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:shop_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{} {}</a>', url, collection.products_count, 'Products')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    autocomplete_fields = ['collection', 'value_feature']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}

    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title', 'min_inventory']
    list_editable = ['unit_price']
    list_filter = ['collection', 'value_feature', 'updated_at', MainFeatureFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    inlines = [FeatureInline]

    def collection_title(self, product):
        if product.collection:
            return product.collection.title
        else:
            return _('No Collection')

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory <= product.min_inventory:
            return _('Low')
        return _('OK')

    @admin.action(description=_('Clear inventory'))
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, _('{count} products were successfully updated.').format(count=updated_count),
                          messages.SUCCESS)

    class Media:
        css = {'all': ['shop/style.css']}


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    exclude = ['deleted_at', 'created_at', 'updated_at']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'membership', 'orders']
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'title', 'parent_review', 'rating']
    list_filter = ['customer', 'product']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    exclude = ['deleted_at', 'updated_at']


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
    list_display = ['id', 'order_link', 'payment_status', 'total_price', 'customer', 'receipt_number']
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
