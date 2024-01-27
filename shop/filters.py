from django.contrib import admin
from django_filters.rest_framework import FilterSet
from django.utils.translation import gettext_lazy as _
from .models import Product, Review, MainFeature


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
            return queryset.filter(main_feature__id=main_feature_id)
