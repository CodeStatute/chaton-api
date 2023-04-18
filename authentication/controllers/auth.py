from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.views import APIView
from ..serializers import CreateAccountSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from ..services.token import get_tokens


# ! cerates new users
class CreateAccountApiView(APIView):
    def get(self, request, format=None):
        return Response({"message": "server said hi"})

    def post(self, request, format=None):
        serializer = CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

            data = {
                "message": "User created successfully",
                "user": {
                    "id": serializer.data["id"],
                    "username": serializer.data["username"],
                    "email": serializer.data["email"],
                    "connection_id": serializer.data["connection_id"],
                    "profile": serializer.data["connection_id"],
                }
            }

            return Response(data, status=status.HTTP_201_CREATED)

        except:
            data = {"message": "something went wrong!"}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ! authenticates users
class LoginApiView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            data = serializer.data

            email = data.get("email")

            password = data.get("password")

            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens(user)
                return Response({"token": token}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "invalid user credentials!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"message": "something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
