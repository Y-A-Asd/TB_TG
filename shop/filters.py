from django.contrib import admin
from django_filters.rest_framework import FilterSet
from django.utils.translation import gettext_lazy as _
from .models import Product, Review, MainFeature, FeatureValue


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt'],
        }


class MainFeatureFilter(admin.SimpleListFilter):
    title = _('Main Feature')
    parameter_name = 'main_feature'

    def lookups(self, request, model_admin):
        return [(main_feature.id, str(main_feature)) for main_feature in MainFeature.objects.all()]

    def queryset(self, request, queryset):
        main_feature_id = self.value()
        if main_feature_id:
            return queryset.filter(main_feature_id=main_feature_id)


class ValueFeatureFilter(admin.SimpleListFilter):
    title = _('Value Feature')
    parameter_name = 'value_feature'

    def lookups(self, request, model_admin):
        return [(value_feature.id, str(value_feature)) for value_feature in FeatureValue.objects.all()]

    def queryset(self, request, queryset):
        value_feature_id = self.value()
        if value_feature_id:
            return queryset.filter(value_feature_id=value_feature_id)