from django.contrib import admin
from django.urls import include, path
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="API documentation with Swagger",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    path("api/", include("users.urls")),
    path("api/", include("addresses.urls")),
    path("api/", include("cards.urls")),
    path("api/", include("products.urls")),
    path("api/", include("cart.urls")),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"
    ),
]
