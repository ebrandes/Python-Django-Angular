from django.contrib.auth import authenticate
from django.http import JsonResponse
from users.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


@swagger_auto_schema(
    method="POST",
    operation_summary="Login User",
    operation_description="Authenticate a user and return a JWT token.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["email", "password"],
    ),
    responses={200: "User logged in", 401: "Invalid credentials"},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate a user and return a JWT token.
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"message": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        response = JsonResponse(
            {
                "user_id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
            }
        )

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="None",
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            samesite="Strict",
            secure=True,
        )

        return response

    return Response(
        {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["POST"])
def logout_user(request):
    response = JsonResponse({"message": "Logged out successfully"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    # Ensure cookies are removed even if HttpOnly is set
    response.set_cookie("access_token", "", max_age=0)
    response.set_cookie("refresh_token", "", max_age=0)

    return response
