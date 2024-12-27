from django.shortcuts import render
from core.functions import success_response_data, error_response_data, generate_serializer_errors, get_tokens_for_user
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import CreateAccountSerializer, LoginSerializer


@swagger_auto_schema(
    method="post",
    request_body=CreateAccountSerializer,
    operation_description="Signup form",
    consumes=['application/x-www-form-urlencoded', 'multipart/form-data'],
)
@api_view(['POST'])
@permission_classes((AllowAny, ))
def create_account(request):
    serializer = CreateAccountSerializer(data=request.data)
    if serializer.is_valid():
        player_data = serializer.create(validated_data=serializer.validated_data)
        response_data = success_response_data(data=player_data, message="Account created")
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response_data = error_response_data(errors=generate_serializer_errors(serializer._errors), description="Validation error")
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=LoginSerializer,
    operation_description="Login form",
    consumes=['application/x-www-form-urlencoded', 'multipart/form-data'],
)
@api_view(['POST'])
@permission_classes((AllowAny, ))
def login_account(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            data = get_tokens_for_user(user=user)
            response_data = success_response_data(data=data, message="Login success")
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = error_response_data(errors={"password": "Password doesn't match"})
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    else:
        response_data = error_response_data(errors=generate_serializer_errors(serializer._errors), description="Validation error")
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
