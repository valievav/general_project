from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Creates new user in a system
    """
    serializer_class = UserSerializer
