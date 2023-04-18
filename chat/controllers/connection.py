from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user.models import User, UserRelation
from ..serializers import FindConnectionSerializer, GetChatRoomMessageSerializer
from user.serializers import GetUserSerializer
from ..models import Chat

# ! find the connection to make new connection


class FindConnectionApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_connection_id = request.user.connection_id

            user_connection_id = f"{user_connection_id}".strip()

            connection_id = request.data.get("connection_id")

            connection_id = f"{connection_id}".strip()

            if user_connection_id == connection_id:
                return Response({"message": "You cannon connect with your own Id!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            user = User.objects.get(connection_id=connection_id)

            to_user = user
            from_user = request.user

            following = UserRelation.objects.filter(
                Q(from_user=from_user) & Q(to_user=to_user)
            )

            follower = UserRelation.objects.filter(
                Q(from_user=to_user) & Q(to_user=from_user)
            )

            data = FindConnectionSerializer(user).data

            respnse_data = {
                "message": "connection found!",
                "data": {
                    **data,
                    "connected": False
                }
            }

            if following or follower:
                respnse_data["data"]["connected"] = True
                return Response(respnse_data, status=status.HTTP_200_OK)

            return Response(respnse_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "No connection found with this Id!"}, status=status.HTTP_404_NOT_FOUND)

        except ValueError:
            return Response({"message": "Invalid connection Id!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except:
            return Response({"message": "something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ! get data of an authenticated user
class MakeNewConnectionApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            to_user_id = request.data.get("to_user")

            from_user = request.user

            to_user = User.objects.get(pk=to_user_id)

            following = UserRelation.objects.filter(
                Q(from_user=from_user) & Q(to_user=to_user)
            )

            follower = UserRelation.objects.filter(
                Q(from_user=to_user) & Q(to_user=from_user)
            )

            data = GetUserSerializer(to_user).data

            respnse_data = {
                "message": "connected successfully!",
                "data": {
                    **data,
                    "connected": True
                }
            }

            if following or follower:
                respnse_data["message"] = "already connected!"
                return Response(respnse_data, status=status.HTTP_200_OK)

            relationship = UserRelation.objects.create(
                from_user=from_user, to_user=to_user)

            return Response(respnse_data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ! get all the chat connections
class GetChatConnectionsApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            following = UserRelation.objects.filter(from_user=request.user)

            followers = UserRelation.objects.filter(to_user=request.user)

            connections = []

            for user in following:
                item = GetUserSerializer(user.to_user).data
                item["chat_room_id"] = user.chat_room_id
                connections.append(item)

            for user in followers:
                item = GetUserSerializer(user.from_user).data
                item["chat_room_id"] = user.chat_room_id
                connections.append(item)

            if not connections:
                return Response({"message": "there's connection found!"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "all the connections", "connections": connections}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ! get all the chat messages
class GetChatRoomMessages(APIView):
    def post(self, request):
        chat_room_id = request.data.get("chat_room_id")

        records = Chat.objects.filter(
            chat_room_id=chat_room_id).order_by("created_at")

        count = records.count() - 10

        records = records[count:]

        data = []

        for message in records:
            item = GetChatRoomMessageSerializer(message).data
            data.append(item)

        respnse_data = {
            "message": "all messages",
            "data": data
        }

        return Response(respnse_data, status=status.HTTP_200_OK)
