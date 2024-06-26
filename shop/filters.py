from django.contrib import admin
from django.db.models import QuerySet, F, Q
from django_filters.rest_framework import FilterSet, BooleanFilter
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import BaseFilterBackend

from .models import Product, Review, MainFeature, Collection, Customer
from django_filters.rest_framework import DjangoFilterBackend


class ProductFilter(FilterSet):
    secondhand = BooleanFilter(field_name='secondhand')
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt'],
            'secondhand': ['exact'],
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


class CustomerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_staff:
            return queryset
        customer = Customer.objects.get(user=user)
        return queryset.filter(customer=customer)


class CollectionFilter(admin.SimpleListFilter):
    title = "Collection"
    parameter_name = "collection"

    def lookups(self, request, model_admin):
        return Collection.objects.values_list("id", "id")

    def get_child_collection_ids(self, collection_id):
        child_collection_ids = set()
        try:
            collection = Collection.objects.get(id=collection_id)
            child_collection_ids.add(collection.id)
            children = collection.subcollection.all()
            for child in children:
                child_collection_ids.update(self.get_child_collection_ids(child.id))
        except Collection.DoesNotExist:
            pass
        return child_collection_ids

    def queryset(self, request, queryset):
        if self.value():
            try:
                collection_id = self.value()
                child_collection_ids = self.get_child_collection_ids(collection_id)
                queryset = queryset.filter(collection_id__in=child_collection_ids)
            except Collection.DoesNotExist:
                pass
        return queryset
