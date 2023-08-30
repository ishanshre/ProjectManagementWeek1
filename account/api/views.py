from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.serializers.serializers import (
    BaseUserSerializer,
    DepartmentSerializer,
    ProfileSerializer,
    UserCreateSerializer,
    UserEditSerializer,
    UserFullSerializer,
    UserListSerializer,
)
from account.models import Department, Profile, User


class UserApiView(generics.ListCreateAPIView):
    serializer_class = BaseUserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        serializer = UserListSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserEditApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserEditSerializer
    queryset = User.objects.all()


class ProfileEditApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class UserFullDetailApiView(APIView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        user = User.objects.get(pk=pk)
        serializer = UserFullSerializer(user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
