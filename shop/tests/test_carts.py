import uuid
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
import pytest
from model_bakery import baker

from discount.models import BaseDiscount
from shop.models import Product, CartItem


@pytest.fixture()
def create_cart(api_client):
    def wrapper():
        return api_client.post(
            '/shop/cart/',
            {},
            format='json'
        )

    return wrapper


@pytest.fixture()
def create_cartitems(api_client, create_cart):
    def wrapper(product_id, quantity):
        cart_id = create_cart().data['id']
        return api_client.post(
            f'/shop/cart/{cart_id}/items/',
            {
                "product_id": product_id,
                "quantity": quantity
            },
            format='json'
        )

    return wrapper


@pytest.mark.django_db
class TestCreateCart:

    def test_if_data_is_valid_returns_201(self, api_client, create_cart):
        response = create_cart()
        assert response.status_code == status.HTTP_201_CREATED
        uuid.UUID(response.data['id'], version=4)


@pytest.mark.django_db
class TestAddingToCart:
    def test_adding_item_to_cart_return_201(self, api_client, create_cartitems):
        product = baker.make(Product)
        response = create_cartitems(product_id=product.id, quantity=1)
        assert response.status_code == status.HTTP_201_CREATED

    def test_adding_invalid_item_to_cart_return_400(self, api_client, create_cartitems):
        product = baker.make(Product)
        response = create_cartitems(product_id=product.id, quantity=0)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdatingCart:

    def test_update_item_to_cart_return_200(self, api_client, create_cartitems):
        response = api_client.post(
            '/shop/cart/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        cart_id = response.data['id']
        product = baker.make(Product, inventory=10)
        response = api_client.post(
            f'/shop/cart/{cart_id}/items/',
            {
                "product_id": product.id,
                "quantity": 1
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        response = api_client.patch(
            f'/shop/cart/{cart_id}/items/{product.id}/',
            {
                "quantity": 2
            },
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        item = CartItem.objects.get(product_id=product.id)
        assert item.quantity == 2


@pytest.mark.django_db
class TestCartDetail:
    def test_cart_detail_return_201(self, api_client, create_cartitems, auth):
        auth(is_staff=True)
        response = api_client.post(
            '/shop/cart/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        cart_id = response.data['id']
        product = baker.make(Product)
        response = api_client.post(
            f'/shop/cart/{cart_id}/items/',
            {
                "product_id": product.id,
                "quantity": 1
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        response = api_client.get(
            f'/shop/cart/{cart_id}/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'items' in response.data


    def test_cart_discount_valid(self, api_client, create_cartitems, auth):
        now = timezone.now()
        valid_from = now - timedelta(days=10)
        valid_to = now + timedelta(days=10)
        discount = BaseDiscount.objects.create(discount=10, code='discount', limit_price=1, max_price=1000,
                                               valid_from=valid_from, valid_to=valid_to)
        auth(is_staff=True)
        response = api_client.post(
            '/shop/cart/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        cart_id = response.data['id']
        product = baker.make(Product)
        response = api_client.post(
            f'/shop/cart/{cart_id}/items/',
            {
                "product_id": product.id,
                "quantity": 1
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        response = api_client.get(
            f'/shop/cart/{cart_id}/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'items' in response.data

        response = api_client.post(
            f'/shop/cart/{cart_id}/apply_discount/',
            {"discount_code": discount.code},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK

        response = api_client.get(
            f'/shop/cart/{cart_id}/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'items' in response.data

    def test_cart_discount_invalid(self, api_client, create_cartitems, auth):
        now = timezone.now()
        valid_from = now - timedelta(days=10)
        valid_to = now + timedelta(days=10)
        discount = BaseDiscount.objects.create(discount=10, code='discount', limit_price=1, max_price=1000)
        auth(is_staff=True)
        response = api_client.post(
            '/shop/cart/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        cart_id = response.data['id']
        product = baker.make(Product)
        response = api_client.post(
            f'/shop/cart/{cart_id}/items/',
            {
                "product_id": product.id,
                "quantity": 1
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        response = api_client.get(
            f'/shop/cart/{cart_id}/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'items' in response.data

        response = api_client.post(
            f'/shop/cart/{cart_id}/apply_discount/',
            {"discount_code": discount.code},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client.post(
            f'/shop/cart/{cart_id}/apply_discount/',
            {"discount_code": 'a', },
            format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = api_client.get(
            f'/shop/cart/{cart_id}/apply_discount/',
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK