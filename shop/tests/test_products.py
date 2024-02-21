from django.utils.translation import activate

from shop.models import Product, Collection, FeatureKey, FeatureValue, MainFeature
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.fixture()
def create_product(api_client, language_code):
    def wrapper(product_title, unit_price, inventory):
        return api_client.post(
            '/api-v1/products/',
            {
                "translations": {language_code: product_title},
                'org_price': unit_price,
                'inventory': inventory
            },
            format='json'
        )

    return wrapper


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_anonymous_return_401(self, create_product):
        # Arrange:preparing -> like create object for test
        # Act:Behaviour
        # Assert:Check response
        response = create_product({'title': 'a'}, 1000, 10)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_return_403(self, api_client, create_product, auth):
        auth()
        response = create_product({'title': 'a'}, 1000, 10)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, create_product, auth):
        auth(is_staff=True)
        response = create_product({'title': ''}, 1000, 10)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['translations'] is not None

    def test_if_data_is_valid_returns_201(self, api_client, create_product, auth):
        auth(is_staff=True)
        response = create_product({'title': 'aaa'}, 1000.00, 10)
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_return_200(self, api_client):
        product = baker.make(Product)
        response = api_client.get(f'/api-v1/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCompareProducts:
    def test_compare_view(self, api_client, create_product):
        activate('en')
        collection = baker.make(Collection)
        product1 = baker.make(Product, id=1, collection=collection)
        product2 = baker.make(Product, id=2, collection=collection)
        key = FeatureKey.objects.create(
            key='test'
        )

        value = FeatureValue.objects.create(
            value='test value',
            key=key
        )

        main_feature = MainFeature.objects.create(
            product=product1,
            key=key,
            value=value
        )
        main_feature = MainFeature.objects.create(
            product=product2,
            key=key,
            value=value
        )
        response = api_client.get(f'/api-v1/compare/?product_ids=1&product_ids=2')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestFilterProducts:
    def test_filter_view(self, api_client, create_product):
        collection = baker.make(Collection)
        product1 = baker.make(Product, id=1, collection=collection)
        product2 = baker.make(Product, id=2, collection=collection)
        key = FeatureKey.objects.create(
            key='test'
        )
        value = FeatureValue.objects.create(
            value='test value',
            key=key
        )

        main_feature = MainFeature.objects.create(
            product=product1,
            key=key,
            value=value
        )
        main_feature = MainFeature.objects.create(
            product=product2,
            key=key,
            value=value
        )

        response = api_client.get(f'/api-v1/products/?collection_id={collection.id}')
        assert response.status_code == status.HTTP_200_OK
        response = api_client.get(f'/api-v1/products/?unit_price__lt=100000&unit_price__gt=10')
        assert response.status_code == status.HTTP_200_OK
        response = api_client.get(f'/api-v1/products/?search=a')
        assert response.status_code == status.HTTP_200_OK
        response = api_client.get(f'/api-v1/products/?feature_key={key.id}')
        assert response.status_code == status.HTTP_200_OK
        response = api_client.get(f'/api-v1/products/?feature_value={value.id}')
        assert response.status_code == status.HTTP_200_OK
        response = api_client.get(f'/api-v1/products/?secondhand=true')
        assert response.status_code == status.HTTP_200_OK
        response = api_client.get(f'/api-v1/products/?ordering=best_sales')
        assert response.status_code == status.HTTP_200_OK
