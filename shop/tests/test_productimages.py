import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError as restValidationError

from shop.models import Product, ProductImage, validate_file_size


@pytest.mark.django_db
def test_product_image_model():
    # Create a Product instance
    product = Product.objects.create(
        unit_price=100.00,
        inventory=10,
    )

    # Create a valid image file
    valid_image = SimpleUploadedFile("valid_image.jpg", b"valid content", content_type="image/jpeg")

    # Create a ProductImage instance with a valid image
    product_image = ProductImage.objects.create(product=product, image=valid_image)

    # Check if the ProductImage is saved correctly

    assert product_image.product == product
    assert "shop/images/valid_image" in product_image.image.name

    # Create an invalid image file (larger than the allowed size)
    invalid_image = SimpleUploadedFile("invalid_image.jpg", b"invalid content" * 1024 * 100, content_type="image/jpeg")

    # Test the validate_file_size function with an invalid image
    with pytest.raises(restValidationError, match="File is large: max size = 500KB!"):
        validate_file_size(invalid_image)

