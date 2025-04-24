import string
import secrets
from apps.common.models import BaseModel
from typing import Type

def generate_unique_code(model:Type[BaseModel],field:str) -> str:
    allowed_chars = string.ascii_letters + string.digits
    unique_code=''.join(secrets.choice(allowed_chars) for _ in range(12))
    if not model.objects.filter(**{field:unique_code}).exists():
        return unique_code
    return generate_unique_code(model,field)