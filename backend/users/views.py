from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from helpers.swagger import get_auth_header


@swagger_auto_schema(
    method="get",
    operation_summary="List All Users",
    operation_description="Retrieve a list of all users.",
    operation_id="user_list",
    manual_parameters=[get_auth_header()],
    responses={200: UserSerializer(many=True)},
)
@api_view(["GET"])
def user_list(request):
    """Handles GET (list users)"""
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    method="post",
    operation_summary="Create a New User",
    operation_description="Create a new user with the provided data.",
    request_body=UserSerializer,
    responses={201: UserSerializer(), 400: "Invalid input"},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    """Handles GET (list users) and POST (create user)"""
    if request.method == "POST":
        """Create a new user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    operation_summary="Get User by ID",
    operation_description="Retrieve user details by ID.",
    manual_parameters=[
        openapi.Parameter(
            "id",
            openapi.IN_PATH,
            description="User ID",
            type=openapi.TYPE_STRING,
        ),
        get_auth_header(),
    ],
    responses={200: UserSerializer(), 404: "User not found"},
)
@api_view(["GET"])
def user_detail(_, id):
    """Handles GET (retrieve user by ID)"""
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"message": "User not found"}
        )

    serializer = UserSerializer(user)
    return Response(serializer.data)


@swagger_auto_schema(
    methods=["put", "patch"],
    operation_summary="Update User",
    operation_description="Update user details with full (`PUT`) or partial (`PATCH`) update.",
    request_body=UserSerializer,
    manual_parameters=[
        openapi.Parameter(
            "id", openapi.IN_PATH, description="User ID", type=openapi.TYPE_STRING
        ),
        get_auth_header(),
    ],
    responses={200: UserSerializer(), 400: "Invalid input", 404: "User not found"},
)
@api_view(["PUT", "PATCH"])
def update_user(request, id):
    """Handles GET (retrieve user), PUT (update user), PATCH (partial update)"""
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"message": "User not found"}
        )

    if request.method in ["PUT", "PATCH"]:
        serializer = UserSerializer(
            user, data=request.data, partial=(request.method == "PATCH")
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="delete",
    operation_summary="Delete User by ID",
    operation_description="Retrieve user details by ID.",
    manual_parameters=[
        openapi.Parameter(
            "id",
            openapi.IN_PATH,
            description="User ID",
            type=openapi.TYPE_STRING,
        ),
        get_auth_header(),
    ],
    responses={200: UserSerializer(), 404: "User not found"},
)
@api_view(["DELETE"])
def delete_user(_, id):
    """Handles DELETE (delete user)"""
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"message": "User not found"}
        )

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
