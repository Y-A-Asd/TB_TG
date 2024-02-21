from core.models import User
from rest_framework import status
import pytest
from model_bakery import baker
from shop.models import Review, Product

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
def create_review(api_client, language_code):
    """
    def create_review(api_client):
        def wrapper(collection):
            return api_client.post('/api-v1/collections/', collection)
    """

    def wrapper(parent=None, rate=4):
        product = baker.make(Product)
        return api_client.post(
            f'/api-v1/products/{product.id}/reviews/',
            {
                "parent_review": parent,
                "title": "sdf",
                "description": "asldkfj",
                "rating": rate
            },
            format='json'  # Specify JSON format explicitly
        )

    return wrapper


@pytest.mark.django_db
class TestCreateReview:
    def test_if_user_anonymous_return_401(self, create_review):
        # Arrange:preparing -> like create object for test
        # Act:Behaviour
        # Assert:Check response
        # with pytest.raises(ValidationError):
        response = create_review()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_returns_201(self, api_client, create_review, auth):
        user = baker.make(User)
        api_client.force_authenticate(user)

        response = create_review()
        # print(response.data)
        # response.active = True
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveReview:
    def test_retrieve_review_with_replies(self, api_client, create_review):
        user = baker.make(User)
        api_client.force_authenticate(user)
        product = baker.make(Product)

        parent_review = api_client.post(
            f'/api-v1/products/{product.id}/reviews/',
            {
                "parent_review": None,
                "title": "sdf",
                "description": "asldkfj",
                "rating": 3
            },
            format='json'
        )
        parent_review_id = parent_review.data['id']
        review = Review.objects.get(id=parent_review_id)
        review.active = True
        review.save()
        reply = api_client.post(
            f'/api-v1/products/{product.id}/reviews/',
            {
                "parent_review": parent_review_id,
                "title": "sdf",
                "description": "asldkfj",
                "rating": 3
            },
            format='json'
        )
        child_review_id = reply.data['id']
        review = Review.objects.get(id=child_review_id)
        review.active = True
        review.save()
        response = api_client.get(
            f'/api-v1/products/{product.id}/reviews/{parent_review_id}/')

        assert response.status_code == status.HTTP_200_OK
        assert 'replies' in response.data

    def test_retrieve_inactive_review(self, api_client):
        user = baker.make(User)
        api_client.force_authenticate(user)
        product = baker.make(Product)

        parent_review = api_client.post(
            f'/api-v1/products/{product.id}/reviews/',
            {
                "parent_review": None,
                "title": "sdf",
                "description": "asldkfj",
                "rating": 3
            },
            format='json'
        )
        parent_review_id = parent_review.data['id']
        response = api_client.get(
            f'/api-v1/products/{product.id}/reviews/{parent_review_id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_replies(self, api_client, create_review):
        user = baker.make(User)
        api_client.force_authenticate(user)
        product = baker.make(Product)

        parent_review = api_client.post(
            f'/api-v1/products/{product.id}/reviews/',
            {
                "parent_review": None,
                "title": "sdf",
                "description": "asldkfj",
                "rating": 3
            },
            format='json'
        )
        parent_review_id = parent_review.data['id']
        review = Review.objects.get(id=parent_review_id)
        review.active = True
        review.save()
        reply = api_client.post(
            f'/api-v1/products/{product.id}/reviews/',
            {
                "parent_review": parent_review_id,
                "title": "sdf",
                "description": "asldkfj",
                "rating": 3
            },
            format='json'
        )
        child_review_id = reply.data['id']
        review = Review.objects.get(id=child_review_id)
        review.active = True
        review.save()
        response = api_client.get(
            f'/api-v1/products/{product.id}/reviews/{parent_review_id}/')

        assert response.status_code == status.HTTP_200_OK
        assert 'replies' in response.data

        response = api_client.get(
            f'/api-v1/products/{product.id}/reviews/{parent_review_id}/replies/')

        assert response.status_code == status.HTTP_200_OK