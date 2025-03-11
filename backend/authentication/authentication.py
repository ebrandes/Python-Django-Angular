from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that retrieves tokens from HttpOnly cookies.
    """

    def authenticate(self, request):
        token = request.COOKIES.get("access_token")  # ✅ Get token from cookies
        if not token:
            return None  # No authentication needed for unauthenticated routes

        validated_token = self.get_validated_token(token)
        return self.get_user(validated_token), validated_token
