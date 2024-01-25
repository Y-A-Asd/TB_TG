from rest_framework.exceptions import ValidationError
from tags.models import Tag, TaggedItem
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType


def validate_file_size(file):
    max_size_kb = 500

    if file.size > max_size_kb * 1024:
        raise ValidationError(f"File is large: max size = {max_size_kb}KB!")


def get_allowed_content_types(tag_label):
    """
    HERE ANOTHER MAGIC :-)
    """
    allowed_content_types = []

    try:
        tag = Tag.objects.get(label=tag_label)
    except Tag.DoesNotExist:
        raise ValidationError(_(f"Tag with label '{tag_label}' does not exist."))

    tagged_items = TaggedItem.objects.filter(tag=tag)
    # print(tagged_items)

    for tagged_item in tagged_items:
        content_type = tagged_item.content_type.model_class()
        # print(content_type)
        if issubclass(content_type, ContentType):
            # print("!!!!")
            models = ContentType.objects.get(id=tagged_item.object_id)
            # print(models)
            # print(tagged_item.object_id)
            model_class = models.model_class()
            # print(model_class)
            allowed_content_types.append(model_class)

    return allowed_content_types


def validate_allowed_content_type(model, tag_label):
    allowed_content_types = get_allowed_content_types(tag_label)
    # print(allowed_content_types)
    # print(model, allowed_content_types)
    if model not in allowed_content_types:
        raise ValidationError(_(f"{model} is not an allowed content type for discounts."))

# validate_allowed_content_type(Product, "special_tag")
