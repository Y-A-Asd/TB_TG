from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError, ErrorDetail
import pytest
from model_bakery import baker
from shop.models import Product, Collection
from tags.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType
from shop.validator import validate_allowed_content_type


@pytest.fixture()
def create_tagged_item():
    tag = baker.make(Tag)
    object = ContentType.objects.get_for_model(Product)
    content_type = ContentType.objects.get_for_model(ContentType)
    taggeditem = TaggedItem.objects.create(tag=tag, content_type=content_type, object_id=object.id)
    return tag


@pytest.mark.django_db
def test_validate_allowed_content_type(create_tagged_item):
    tag = create_tagged_item
    # print(tag)
    with pytest.raises(ValidationError):
        validate_allowed_content_type(Collection, tag.label)
    validate_allowed_content_type(Product, tag.label)
