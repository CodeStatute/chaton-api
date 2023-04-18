from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import User
from ..serializers import GetUserSerializer


# ! update the profile picture
class UploadProfileApiView(APIView):
    def put(self, request, pk, format=None):
        try:
            # profile_photo = (request.FILES['profile'])
            profile_photo = request.data['profile']
            user = User.objects.get(pk=pk)
            user.profile = profile_photo
            user.save()
            return Response({"message": "profile picture has been saved."}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({"message": "something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ! get data of an authenticated user
class GetUserInfoApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            pk = request.user.id

            user = User.objects.get(pk=pk)

            data = GetUserSerializer(user).data

            respnse_data = {
                "message": "user info!",
                "data": {
                    **data
                }
            }

            return Response(respnse_data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
