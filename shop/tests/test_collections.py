from django.contrib.auth.models import User
from rest_framework import status
import pytest
from model_bakery import baker
from shop.models import Collection

"""
ALWAYS TEST BEHAVIOUR, NOT IMPLEMENTATION
""""""
ALWAYS TEST BEHAVIOUR, NOT IMPLEMENTATION
""""""
ALWAYS TEST BEHAVIOUR, NOT IMPLEMENTATION
""""""
ALWAYS TEST BEHAVIOUR, NOT IMPLEMENTATION
""""""
ALWAYS TEST BEHAVIOUR, NOT IMPLEMENTATION
""""""
ALWAYS TEST BEHAVIOUR, NOT IMPLEMENTATION
"""


@pytest.fixture()
def create_collection(api_client, language_code):
    """
    def create_collection(api_client):
        def wrapper(collection):
            return api_client.post('/shop/collections/', collection)
    """

    def wrapper(collection_data):
        return api_client.post(
            '/shop/collections/',
            {
                "translations": {language_code: collection_data}
            },
            format='json'  # Specify JSON format explicitly
        )

    return wrapper


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_anonymous_return_401(self, create_collection):
        # Arrange:preparing -> like create object for test
        # Act:Behaviour
        # Assert:Check response
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_return_403(self, api_client, create_collection, auth):
        auth()
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, create_collection, auth):
        auth(is_staff=True)
        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['translations'] is not None

    def test_if_data_is_valid_returns_201(self, api_client, create_collection, auth):
        auth(is_staff=True)
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/shop/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        # assert response.data == {
        #     'id': collection.id,
        #     'title': collection.title,
        #     'products_count': 0,
        #     'parent': None
        # }
