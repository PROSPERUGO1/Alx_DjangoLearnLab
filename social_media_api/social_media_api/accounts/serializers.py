# My code
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "bio"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            bio=validated_data.get(
                "bio", ""
            ),  # safely provides an empty string fallback if the bio is missing because of blank=True in my model
        )
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # We only expose the fields they are allowed to change after registration
        fields = ["bio", "profile_picture", "first_name", "last_name"]

# Checker code
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token  # 1. Added the requested import


class UserRegistrationSerializer(serializers.ModelSerializer):
    # 2. Explicitly calling serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        # Note: If the checker complains about profile_picture, remove it from this list,
        # but try it with it first since it was in your model requirements.
        fields = ["username", "email", "password", "bio", "profile_picture"]

    def create(self, validated_data):
        # 3. The checker wants this exact literal string chained together
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            profile_picture=validated_data.get("profile_picture", None),
        )

        # 4. Minting the token immediately upon user creation
        Token.objects.create(user=user)

        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["bio", "profile_picture", "first_name", "last_name"]
"""