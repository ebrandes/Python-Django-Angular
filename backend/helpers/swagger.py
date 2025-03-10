from drf_yasg import openapi


def get_auth_header():
    """
    Returns the standard Authorization header for Swagger documentation.
    """
    return openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description="Token format: Bearer <token>",
        type=openapi.TYPE_STRING,
        required=True,
    )
