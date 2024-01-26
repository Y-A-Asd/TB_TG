# import pytest
# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from django.contrib.contenttypes.models import ContentType
# from model_bakery import baker
# from discount.models import BaseDiscount
# from shop.models import Product
#
#
# @pytest.mark.django_db
# class TestDiscountItemsModel(TestCase):
#     def setUp(self):
#         # Create a BaseDiscount with active=True
#         self.base_discount = BaseDiscount.objects.create(
#             discount=10.0,
#             active=True,
#             code='discount_code',
#             valid_from='2024-01-01T00:00:00Z',
#             valid_to='2024-02-01T00:00:00Z',
#             mode=BaseDiscount.Mode.DiscountOff,
#         )
#         self.base_discount = BaseDiscount.objects.create(
#             discount=9.0,
#             active=True,
#             code='discount2_code',
#             valid_from='2024-01-01T00:00:00Z',
#             valid_to='2024-02-01T00:00:00Z',
#             mode=BaseDiscount.Mode.DiscountOff,
#         )
#
#     def test_clean_existing_discount_item(self):
#         # Create an existing DiscountItems with the same content_type, object_id, and active=True
#         product:Product = baker.make(Product)
#         product.discount = self.base_discount
#
#         # Attempt to create a new DiscountItems with the same content_type, object_id, and active=True
#         product.discount = self.base_discount
#
#         # Make sure that calling clean on the new DiscountItems raises a ValidationError
#         with self.assertRaises(ValidationError) as context:
#             product.clean()
#         self.assertEqual(str(context.exception), "['There is already an active discount for this item.']")
