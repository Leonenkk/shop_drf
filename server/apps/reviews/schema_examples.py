from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

REVIEW_PARAM_EXAMPLES = [
    OpenApiParameter(
        "product__slug",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        description="enter product name in slug format",
    ),
    OpenApiParameter(
        "rating__gte",
        OpenApiTypes.INT,
        OpenApiParameter.QUERY,
        description="enter minimum int rating number",
    ),
    OpenApiParameter(
        "rating__lte",
        OpenApiTypes.INT,
        OpenApiParameter.QUERY,
        description="enter maximum int rating number",
    ),
    OpenApiParameter(
        "ordering",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        description="enter fields (created_at,rating); use '-' for descending",
    ),
]
