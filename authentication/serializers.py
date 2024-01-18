from django.contrib.auth.models import User
from rest_framework import serializers
from authentication.social_auth import Google
from django.conf import settings
from courses.custom_functions import generate_random_string

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    sign_up = serializers.BooleanField()

    def validate(self, data):
        auth_token = data.get("auth_token")
        user_data = Google.validate(auth_token)

        print(data.get("sign_up", None))

        try:
            user_data["sub"]
        except Exception as identifier:
            raise serializers.ValidationError({"error": str(identifier)})
        
        if user_data["aud"] not in settings.GOOGLE_CLIENT_ID.split(" "):
            raise serializers.ValidationError("oops, who are you?")

        email = user_data["email"]
        name = user_data["name"]

        user = User.objects.filter(email=email)
        if data.get("sign_up"):
            if user.exists():
                raise serializers.ValidationError({"error": "user already exists"})
            else:
                user = User.objects.create_user(
                    email=email,
                    username = email,
                    full_name=name,
                    password=generate_random_string(12),
                    is_active=False,
                )
                return {"message": "user account created successfully", "user_id": str(user.id)}

        elif not data.get("sign_up"):
            if not user.exists():
                raise serializers.ValidationError({"error": "user does not exists"})
            else:
                user = user.first()
                if user.is_active:
                    return {"message": "login successful", "user_id": user.id}
                else:
                    return {"message": "account not activated", "user_id": str(user.id), "email": user.email}