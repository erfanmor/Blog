from rest_framework.views import APIView
from account.models import CustomUser
from post.models import Post
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema, OpenApiRequest, OpenApiResponse
from .document_example import (CreateUserExample,
                               UserPostListExample,
                               AllUsersExample,
                               UserInfoExample)

from .serializers import (CreateUserSerializer,
                          ListUsersSerializer,
                          PostSerializer,
                          UserSerializer,)


class CreateUserApiView(APIView):
    @extend_schema(
        request=OpenApiRequest(CreateUserSerializer, examples=[CreateUserExample.request]),
        responses={200: OpenApiResponse(CreateUserSerializer, examples=[CreateUserExample.response],)},
        methods=['POST'],
    )
    
    def post(self, request):
        req_data = request.data
        serializer = CreateUserSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        new_user = CustomUser(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        new_user.save()

        return Response(serializer.data)


class UserPostListApiView(APIView):
    @extend_schema(
        request=OpenApiRequest(PostSerializer),
        responses={200: OpenApiResponse(PostSerializer, examples=[
                                        UserPostListExample.response],)},
        methods=['GET']
    )

    def get(self, request, username):
        author_id = CustomUser.objects.get(username=username).id
        data = get_list_or_404(Post, author=author_id)
        serializer = PostSerializer(data, many=True)

        return Response(serializer.data)
    
    # Authentication and permissions config
    permission_classes = [IsAuthenticated]


class AllUsersApiView(APIView):
    @extend_schema(
        request=OpenApiRequest(PostSerializer),
        responses={200: OpenApiResponse(PostSerializer, examples=[AllUsersExample.response],)},
        methods=['GET']
    )

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = ListUsersSerializer(users, many=True)

        return Response(serializer.data)
    
    
class UserInfoApiView(APIView):
    @extend_schema(
        request=OpenApiRequest(PostSerializer),
        responses={200: OpenApiResponse(PostSerializer, examples=[UserInfoExample.response],)},
        methods=['GET']
    )

    def get(self, request, username):
        user_id = CustomUser.objects.get(username=username).id
        user_info = get_object_or_404(CustomUser, id=user_id)

        serializar = UserSerializer(user_info)
        data = serializar.data

        data['SocialMedia'] = {'website': user_info.website,
                               'github': user_info.gitHub,
                               'twitter': user_info.twitter,
                               'instagram': user_info.instagram,
                               'facebook': user_info.facebook, }

        return Response(data)
    
    # Authentication and permissions config
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
