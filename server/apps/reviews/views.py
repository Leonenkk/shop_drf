from django.db.models import Avg, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from apps.reviews.models import Review
from apps.reviews.schema_examples import REVIEW_PARAM_EXAMPLES
from apps.reviews.serializers import ReviewSerializer


@extend_schema(
    tags=["Review"],
    responses={
        401: OpenApiResponse(description="Unauthorized"),
        404: OpenApiResponse(description="Not found"),
    },
)
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = {
        "product__slug": ["exact"],
        "rating": ["gte", "lte"],
    }
    ordering_fields = ("rating", "created_at")
    ordering = ("-created_at",)

    @extend_schema(
        summary="List all reviews",
        description="Returns a list of all reviews in the system.",
        responses={200: ReviewSerializer(many=True)},
        parameters=REVIEW_PARAM_EXAMPLES,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new review",
        description="Creates a new review for authenticated users.",
        request=ReviewSerializer,
        examples=[
            OpenApiExample(
                "example request",
                value={"product": "adidas", "rating": 5, "text": "good service"},
            )
        ],
        responses={
            201: ReviewSerializer,
            400: OpenApiResponse(description="Invalid input data"),
        },
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Retrieve a review",
        description="Get details of a specific review.",
        responses={200: ReviewSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()  # ensure owner filter
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a review",
        description="Partially update a review (only by owner).",
        request=ReviewSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a review",
        description="Delete a review (only by owner)",
    )
    def destroy(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            average_rating=Avg(
                "product__reviews__rating",
                filter=Q(product__reviews__is_deleted=False),
            )
        )
        if self.action in ("retrieve", "partial_update", "destroy"):
            qs = qs.filter(user=self.request.user)
        return qs
