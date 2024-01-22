from rest_framework.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 50

    if file.size > max_size_kb * 1024:
        raise ValidationError(f"File is large: max size = {max_size_kb}KB!")
