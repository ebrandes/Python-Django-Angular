from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import login_user

urlpatterns = [
    path('login/', login_user,  name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
