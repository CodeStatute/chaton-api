from django.urls import path
from .controllers.user import UploadProfileApiView, GetUserInfoApiView


urlpatterns = [
    path("upload-profile/<uuid:pk>/",
         UploadProfileApiView.as_view(), name="upload_profile"),

    path('get-user/',
         GetUserInfoApiView.as_view(), name='get_user_info'),
]
