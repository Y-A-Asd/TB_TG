from django.contrib import admin
from django.db.models import QuerySet, F, Q
from django_filters.rest_framework import FilterSet
from django.utils.translation import gettext_lazy as _
from .models import Product, Review, MainFeature, Collection
from django_filters.rest_framework import DjangoFilterBackend


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt'],
        }


class RecursiveDjangoFilterBackend(DjangoFilterBackend):

    def get_recursive_q(self, collection_id):
        if collection_id:
            q_object = Q(collection_id=collection_id)

            # Include children recursively
            child_collections = Collection.objects.filter(parent_id=collection_id)
            for child_collection in child_collections:
                q_object |= self.get_recursive_q(child_collection.id)

            return q_object

    def get_unit_price_filters(self, request):
        gt_value = request.query_params.get('unit_price__gt')
        lt_value = request.query_params.get('unit_price__lt')
        if gt_value or lt_value:
            filters = Q()

            if gt_value is not None:
                filters &= Q(unit_price__gt=gt_value)

            if lt_value is not None:
                filters &= Q(unit_price__lt=lt_value)

            return filters


class MainFeatureFilter(admin.SimpleListFilter):
    title = _('Main Feature')
    parameter_name = 'main_feature'

    def lookups(self, request, model_admin):
        return [(main_feature.id, str(main_feature)) for main_feature in MainFeature.objects.all()]

    def queryset(self, request, queryset):
        main_feature_id = self.value()
        if main_feature_id:
            return queryset.filter(main_feature__id=main_feature_id)


class InventoryFilter(admin.SimpleListFilter):
    title = _('Inventory')
    parameter_name = 'inventory'
    exclude = ['deleted_at', 'created_at', 'updated_at']

    def lookups(self, request, model_admin):
        return [
            ('<min', _('Low')),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<min':
            return queryset.filter(inventory__lt=F('min_inventory'))
