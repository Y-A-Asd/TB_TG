from django import forms
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from tags.models import TaggedItem
from . import models
from .models import CartItem, Cart, Review, BaseDiscount, DiscountItems


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    verbose_name = _('Tag')
    verbose_name_plural = _('Tags')


class InventoryFilter(admin.SimpleListFilter):
    title = _('Inventory')
    parameter_name = 'inventory'
    exclude = ['deleted_at', 'created_at', 'updated_at']
    inlines = [TagInline]

    def lookups(self, request, model_admin):
        return [
            ('<10', _('Low')),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Promotion)
class PromotionAdmin(TranslatableAdmin):
    list_display = ('title', 'description')
    inlines = [TagInline]


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']
    inlines = [TagInline]

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

    actions = ['Clear inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'updated_at', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']
    exclude = ['deleted_at', 'created_at', 'updated_at']
    inlines = [TagInline]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
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
    autocomplete_fields = ['parent']
    list_display = ['title', 'products_count']
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


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    exclude = ['deleted_at', 'created_at', 'updated_at']
    inlines = [TagInline]

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
    max_num = 10
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ['deleted_at', 'updated_at']
    autocomplete_fields = ['customer']
    list_filter = ['customer']
    inlines = [OrderItemInline, TagInline]
    list_display = ['id', 'created_at', 'customer']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    exclude = ['deleted_at', 'created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'view_cart']
    list_filter = ['cart', 'product']
    exclude = ['deleted_at', 'created_at', 'updated_at']

    def view_cart(self, obj):
        cart_url = reverse('admin:shop_cart_change', args=[obj.cart.id])
        return format_html('<a href="{}">View Cart Items</a>', cart_url)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'view_cart_items']
    readonly_fields = ['view_cart_items']
    inlines = [CartItemInline]
    exclude = ['deleted_at', 'created_at', 'updated_at']

    def view_cart_items(self, obj):
        cart_items_url = reverse('admin:shop_cartitem_changelist') + f'?cart__id__exact={obj.id}'
        return format_html('<a href="{}">View Cart Items</a>', cart_items_url)

    view_cart_items.short_description = 'Cart Items'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'name', 'parent_review']
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
            raise ValidationError({'discount': 'Invalid discount!(Check Mode again)'})

        if mode == BaseDiscount.Mode.DiscountOff and discount > 99:
            raise ValidationError({'discount': 'Invalid discount(Check Mode again)'})

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
