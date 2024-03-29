import os
from rest_framework.exceptions import ValidationError


def get_path_ava_url(instance, file):
    return f'ava/{instance.id}/{file}'


def validate_ava_img(obj):
    megabite_limit = 2

    if obj.size > megabite_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла не должен превышать {megabite_limit} мб")


def delete_old_ava_path(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)