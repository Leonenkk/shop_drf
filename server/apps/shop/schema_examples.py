from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

from core import settings

PRODUCT_PARAM_EXAMPLES = [
    OpenApiParameter(
        name="max_price",
        description="The maximum price of the product.",
        type=OpenApiTypes.INT,
        required=False,
    ),
    OpenApiParameter(
        name="min_price",
        description="The minimum price of the product.",
        type=OpenApiTypes.INT,
        required=False,
    ),
    OpenApiParameter(
        name="in_stock",
        description="How much product is in stock.",
        required=False,
        type=OpenApiTypes.INT,
    ),
    OpenApiParameter(
        name="created_at",
        description="When the product was created.",
        required=False,
        type=OpenApiTypes.DATE,
    ),
    OpenApiParameter(
        name="page_size",
        description=f"The amount of item per page you want to display. Defaults to {settings.REST_FRAMEWORK['PAGE_SIZE']}",
        type=OpenApiTypes.INT,
        required=False,
    ),
]
