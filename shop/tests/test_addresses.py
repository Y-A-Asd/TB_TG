from core.models import User
from rest_framework import status
import pytest
from model_bakery import baker
from shop.models import Collection, Customer


@pytest.fixture()
def create_address(api_client):
    def wrapper(zip_code, path, city, province):
        return api_client.post(
            '/api-v1/addresses/',
            {
                'zip_code': zip_code,
                'path': path,
                'city': city,
                'province': province,
            },
            format='json'  # Specify JSON format explicitly
        )

    return wrapper


@pytest.mark.django_db
class TestCreateAddress:
    def test_if_user_anonymous_return_401(self, create_address):
        # Arrange:preparing -> like create object for test
        # Act:Behaviour
        # Assert:Check response
        response = create_address('a', 'a', 'a', 'a', )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_returns_201(self, api_client, create_address, auth):
        user = baker.make(User)
        # customer = baker.make(Customer, user_id=user.id)
        api_client.force_authenticate(user)
        response = create_address('a', 'a', 'a', 'a', )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveAddress:
    def test_if_user_anonymous_return_403(self, create_address, api_client):
        user = baker.make(User)
        api_client.force_authenticate(user)
        response = create_address('a', 'a', 'a', 'a', )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

        address_id = response.data['id']
        user2 = baker.make(User)

        api_client.force_authenticate(user2)

        response = api_client.get(
            f'/api-v1/addresses/{address_id}/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_authenticated_can_retrieve_own_address(self, create_address, api_client):
        user = baker.make(User)
        api_client.force_authenticate(user)

        response = create_address('a', 'a', 'a', 'a', )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        address_id = response.data['id']

        response = api_client.get(
            f'/api-v1/addresses/{address_id}/',
            {},
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == address_id


@pytest.mark.django_db
class TestUpdateAddress:
    def test_if_user_anonymous_return_403(self, create_address, api_client):
        user = baker.make(User)
        api_client.force_authenticate(user)
        response = create_address('a', 'a', 'a', 'a', )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

        address_id = response.data['id']
        user2 = baker.make(User)

        api_client.force_authenticate(user2)

        response = api_client.patch(
            f'/api-v1/addresses/{address_id}/',
            {
                'zip_code': 'new_zip_code',
                'path': 'new_path',
                'city': 'new_city',
                'province': 'new_province',
            },
            format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_authenticated_can_update_own_address(self, create_address, api_client):
        user = baker.make(User)
        api_client.force_authenticate(user)

        response = create_address('a', 'a', 'a', 'a', )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        address_id = response.data['id']

        response = api_client.patch(
            f'/api-v1/addresses/{address_id}/',
            {
                'zip_code': 'new_zip',
                'path': 'new_path',
                'city': 'new_city',
                'province': 'new_province',
            },
            format='json'
        )
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['zip_code'] == 'new_zip'
        assert response.data['path'] == 'new_path'
        assert response.data['city'] == 'new_city'
        assert response.data['province'] == 'new_province'
