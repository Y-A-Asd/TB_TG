from django.contrib.auth import get_user_model
from rest_framework import status
import pytest
from model_bakery import baker

from shop.models import Customer


@pytest.fixture()
def create_customer(api_client):
    def wrapper(customer_first_name, cusotmer_last_name):
        user = baker.make(get_user_model(), id=999999)
        print(user.id)
        return api_client.post(
            '/shop/customers/',
            {
                'user_id': user.id,
                'first_name': customer_first_name,
                'last_name': cusotmer_last_name
            },
            format='json'
        )

    return wrapper


@pytest.mark.django_db
class TestCreateCustomer:
    """i made signal to avoid creating customer"""

    def test_if_user_anonymous_return_401(self, create_customer):
        # Arrange:preparing -> like create object for test
        # Act:Behaviour
        # Assert:Check response
        response = create_customer('t', 'a')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_return_403(self, api_client, create_customer, auth):
        auth()
        response = create_customer('t', 'a')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    # def test_if_data_is_invalid_returns_400(self, api_client, create_customer, auth):
    #     auth(is_staff=True)
    #     response = create_customer('t', '')
    #
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert 'last_name' in response.data
    #     assert False

    # def test_if_data_is_valid_returns_201(self, api_client, create_customer, auth):
    #     auth(is_staff=True)
    #     response = response = create_customer('t', 'a')
    #
    #     assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveCustomers:
    def test_if_customer_exists_return_200(self, api_client, auth):
        auth(is_staff=True)
        user = baker.make(get_user_model(), id=1)
        customer = Customer.objects.get(user_id=user.id)
        response = api_client.get(f'/shop/customers/{customer.id}/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_promotion_exists_and_not_admin_return_200(self, api_client, auth):
        auth()
        user = baker.make(get_user_model(), id=2)
        customer = Customer.objects.get(user_id=user.id)
        response = api_client.get(f'/shop/customers/{customer.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

