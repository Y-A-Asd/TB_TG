import pytest
from django.utils.translation import activate
from shop.models import MainFeature


@pytest.mark.django_db
def test_main_feature_model():

    activate('en')

    main_feature_en = MainFeature(
        title='Test Title',
        description='Test Description',
        value='Test Value'
    )
    main_feature_en.save()

    activate('fa')

    main_feature_fa = MainFeature(
        title='عنوان تست',
        description='توضیحات تست',
        value='مقدار تست'
    )
    main_feature_fa.save()

    saved_main_feature_en = MainFeature.objects.get(id=main_feature_en.id)

    assert saved_main_feature_en.title == 'Test Title'
    assert saved_main_feature_en.description == 'Test Description'
    assert saved_main_feature_en.value == 'Test Value'

    translation_en = saved_main_feature_en.translations.filter(language_code='en').first()
    assert translation_en.title == 'Test Title'
    assert translation_en.description == 'Test Description'
    assert translation_en.value == 'Test Value'

    saved_main_feature_fa = MainFeature.objects.get(id=main_feature_fa.id)

    assert saved_main_feature_fa.title == 'عنوان تست'
    assert saved_main_feature_fa.description == 'توضیحات تست'
    assert saved_main_feature_fa.value == 'مقدار تست'

    translation_fa = saved_main_feature_fa.translations.filter(language_code='fa').first()
    assert translation_fa.title == 'عنوان تست'
    assert translation_fa.description == 'توضیحات تست'
    assert translation_fa.value == 'مقدار تست'
