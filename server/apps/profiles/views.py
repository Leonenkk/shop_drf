from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.serializers import ProfileSerializer


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user=request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request):
        user=request.user
        serializer = self.serializer_class(user, data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user=request.user
        user.is_active=False
        user.save()
        return Response({
            'message':'User deactivated'
        },status=status.HTTP_204_NO_CONTENT
        )
