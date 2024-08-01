from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from users.services.user_service import UserService
from users.serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def list(self, request):
        users = self.user_service.get_all_users()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        user_data = request.data
        user = self.user_service.create_user(user_data)
        return Response(user, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        user = self.user_service.get_user(pk)
        if user is not None:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, partial=False):
        user = self.user_service.get_user(pk)
        if user is not None:
            user_data = request.data
            try:
                updated_user = self.user_service.update_user(pk, user_data, partial=partial)
                return Response(CustomUserSerializer(updated_user).data)
            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        success = self.user_service.delete_user(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
