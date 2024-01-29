import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture()
def language_code():
    return 'en'


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def auth(api_client):
    def do_authenticate(user=User, is_staff=False):
        return api_client.force_authenticate(user=user(is_staff=is_staff))

    return do_authenticate
