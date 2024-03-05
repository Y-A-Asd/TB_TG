import pytest
from decimal import Decimal

from django.db.utils import DataError
from django.utils.translation import activate
from django.core.exceptions import ValidationError
from shop.models import Product, Collection, Promotion, BaseDiscount, MainFeature
from model_bakery import baker


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


@pytest.mark.django_db
def test_product_price_after_off():
    # Create necessary model instances
    collection = Collection.objects.create(title='Test Collection')
    promotion = Promotion.objects.create(title='Test Promotion')
    discount = BaseDiscount.objects.create(discount=10)

    product = Product.objects.create(
        unit_price=1000.00,
        inventory=10,
        collection=collection,
        promotions=promotion,
        discount=discount
    )
    main_feature = baker.make(MainFeature, product=product)

    assert discount.ensure_availability()

    assert product.price_after_off == Decimal(900.00)

    discount.mode = BaseDiscount.Mode.DirectPrice
    discount.discount = 500
    discount.save()

    assert discount.ensure_availability()
    assert product.price_after_off == Decimal(500.00)

    # discount.mode = 'InvalidMode'
    #
    # with pytest.raises((DataError)):
    #     discount.save()
    #     product.price_after_off
