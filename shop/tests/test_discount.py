import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from shop.models import BaseDiscount, DiscountItems


@pytest.mark.django_db
class TestDiscountItemsModel(TestCase):
    def setUp(self):
        # Create a BaseDiscount with active=True
        self.base_discount = BaseDiscount.objects.create(
            discount=10.0,
            active=True,
            code='discount_code',
            valid_from='2024-01-01T00:00:00Z',
            valid_to='2024-02-01T00:00:00Z',
            mode=BaseDiscount.Mode.DiscountOff,
        )

    def test_clean_existing_discount_item(self):
        # Create an existing DiscountItems with the same content_type, object_id, and active=True
        existing_discount_item = DiscountItems.objects.create(
            discount=self.base_discount,
            content_type=ContentType.objects.get_for_model(self.base_discount),
            object_id='some_object_id',
        )

        # Attempt to create a new DiscountItems with the same content_type, object_id, and active=True
        new_discount_item = DiscountItems(
            discount=self.base_discount,
            content_type=ContentType.objects.get_for_model(self.base_discount),
            object_id='some_object_id',
        )

        # Make sure that calling clean on the new DiscountItems raises a ValidationError
        with self.assertRaises(ValidationError) as context:
            new_discount_item.clean()
        print(str(context.exception))
        print(type(context.exception))
        self.assertEqual(str(context.exception), "['There is already an active discount for this item.']")
