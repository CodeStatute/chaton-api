from django.urls import path
from .controllers.auth import CreateAccountApiView, LoginApiView
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)


urlpatterns = [
    path("create-account/",
         CreateAccountApiView.as_view(), name="create_account"),

    path('login/', LoginApiView.as_view(), name='login'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
