from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from user.models import User


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate(self, data):
        user = User(**data)

        password = data.get('password')
        username = data.get('username')

        try:
            validate_password(password=password, user=user)
        except ValidationError as e:
            errors = {'password': list(e.messages)}
            raise serializers.ValidationError(errors)

        if (len(username) < 2):
            raise serializers.ValidationError(
                {'username': 'username is too short.'})

        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]
