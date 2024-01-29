from shop.models import Promotion, Product
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.fixture()
def create_promotion(api_client, language_code):
    def wrapper(promotion_title):
        return api_client.post(
            '/shop/promotions/',
            {
                "translations": {language_code: promotion_title},

            },
            format='json'
        )

    return wrapper


@pytest.mark.django_db
class TestRetrievePromotions:
    def test_if_promotion_exists_return_200(self, api_client):
        promotion = baker.make(Promotion)
        response = api_client.get(f'/shop/promotions/{promotion.id}/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_list_of_product_exist_in_promotion(self, api_client):
        promotion = baker.make(Promotion)
        baker.make(Product, promotions=promotion)
        response = api_client.get(f'/shop/promotions/{promotion.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert 'products' in response.json()
