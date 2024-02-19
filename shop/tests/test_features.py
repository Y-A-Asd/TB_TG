import pytest
from django.utils.translation import activate
from shop.models import MainFeature, FeatureKey, FeatureValue, Product
from model_bakery import baker
from shop.admin import MainFeatureAdminForm


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


@pytest.fixture
def key():
    return FeatureKey.objects.create(key='Test Key')


@pytest.fixture
def value():
    return FeatureValue.objects.create(value='Test Value')


@pytest.mark.django_db
def test_clean_invalid_relationship():
    key = FeatureKey.objects.create(key='Test Key')
    value = FeatureValue.objects.create(value='Test Value', key=key)
    invalid_key = FeatureKey.objects.create(key='Invalid Key')  # Create an invalid key
    form_data = {
        'key': invalid_key,
        'value': value
    }
    form = MainFeatureAdminForm(data=form_data)
    assert not form.is_valid()
    assert 'value' in form.errors


@pytest.mark.django_db
def test_clean_missing_value(key):
    form_data = {
        'key': key,
        'value': None
    }
    form = MainFeatureAdminForm(data=form_data)
    assert not form.is_valid()
    assert 'value' in form.errors
