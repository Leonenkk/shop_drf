from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsOwner
from apps.profiles.serializers import ProfileSerializer

tags = ["Profiles"]


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsOwner,)

    @extend_schema(
        summary="Retrieve profile details",
        description="""
            This endpoint allows a user to retrieve his/her profile.
        """,
        tags=tags,
    )
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update profile details",
        description="""
        This endpoint allows a user to update his/her profile.
        """,
        tags=tags,
    )
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(
            user, data=request.data
        )  # мб добавить partial
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete profile details",
        description="""
        This endpoint allows a user to deactivate his/her profile.
        """,
        tags=tags,
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"message": "User deactivated"}, status=status.HTTP_204_NO_CONTENT
        )
