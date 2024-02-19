import pytest
from rest_framework import status
from model_bakery import baker
from rest_framework.reverse import reverse

from core.models import User
from shop.models import Order, Transaction, Product


@pytest.fixture()
def create_address(api_client):
    def wrapper(zip_code, path, city, province):
        return api_client.post(
            '/shop/addresses/',
            {
                'zip_code': zip_code,
                'path': path,
                'city': city,
                'province': province,
            },
            format='json'
        )

    return wrapper


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
    def wrapper():
        product = baker.make(Product, unit_price=10, inventory=10)
        cart_id = create_cart().data['id']
        return api_client.post(
            f'/shop/cart/{cart_id}/items/',
            {
                "product_id": product.id,
                "quantity": 1
            },
            format='json'
        ), cart_id

    return wrapper


@pytest.fixture()
def create_order(api_client, auth, create_cart, create_cartitems):
    response, cart_id = create_cartitems()

    def wrapper():
        return api_client.post('/shop/orders/',
                               {
                                   'cart_id': cart_id
                               }, format='json')

    return wrapper


@pytest.mark.django_db
class TestCreateOrderWithCart:
    def test_create_order_without_address_return_400(self, api_client, create_order):
        user = baker.make(User, id=2)
        api_client.force_authenticate(user)
        response = create_order()
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_order_without_auth_return_401(self, api_client, create_order):
        response = create_order()
        print(response.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_with_address_return_201(self, api_client, create_order, create_address):
        user = baker.make(User)
        api_client.force_authenticate(user)
        create_address('a', 'a', 'a', 'a', )
        response = create_order()
        assert response.status_code == status.HTTP_201_CREATED

    def test_transaction_create_after_order(self, api_client, create_order, create_address):
        user = baker.make(User)
        api_client.force_authenticate(user)
        create_address('a', 'a', 'a', 'a', )
        response = create_order()
        print('response', response.data)
        print('response', response)
        order_id = response.data['id']
        # transaction = Transaction.objects.filter(order_id=order_id).exists()
        assert Transaction.objects.filter(order_id=order_id).exists()


@pytest.mark.django_db
class TestUpdateOrder:

    def test_update_order_status_return_201(self, api_client, create_order, create_address):
        user = baker.make(User, is_staff=True)
        api_client.force_authenticate(user)
        create_address('a', 'a', 'a', 'a', )
        response = create_order()
        order_id = response.data['id']

        update_data = {
            'order_status': 'S'
        }

        update_url = f'/shop/orders/{order_id}/'
        response = api_client.patch(update_url, update_data, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_200_OK

        updated_order = Order.objects.get(id=order_id)
        assert updated_order.order_status == 'S'

    def test_update_order_status_invalid_data(self, api_client, create_order, create_address):
        user = baker.make(User, is_staff=True)
        api_client.force_authenticate(user)
        create_address('a', 'a', 'a', 'a', )
        response = create_order()
        print(response.data)
        order_id = response.data['id']

        update_data = {
            'order_status': 'invalid_status'
        }

        update_url = f'/shop/orders/{order_id}/'
        response = api_client.patch(update_url, update_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveOrders:

    def test_retrieve_orders_authenticated_user(self, api_client, auth):
        user = baker.make(User)
        api_client.force_authenticate(user)
        order1 = baker.make(Order, customer=user.customer)
        order2 = baker.make(Order, customer=user.customer)

        response = api_client.get('/shop/orders/')
        assert response.status_code == status.HTTP_200_OK

        for order_data in response.data:
            assert 'total_price' in order_data

