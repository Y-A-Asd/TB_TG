import pytest
from django.utils.translation import activate
from shop.models import MainFeature, FeatureKey, FeatureValue, Product
from model_bakery import baker


@pytest.mark.django_db
def test_main_feature_model():
    activate('en')
    key = FeatureKey.objects.create(
        key='test'
    )

    value = FeatureValue.objects.create(
        value='test value',
        key=key
    )

    product = baker.make(Product)
    main_feature = MainFeature.objects.create(
        product=product,
        key=key,
        value=value
    )
    saved_main_feature_en = MainFeature.objects.get(id=main_feature.id)

    assert saved_main_feature_en.key.key == 'test'
    assert saved_main_feature_en.value.value == 'test value'
