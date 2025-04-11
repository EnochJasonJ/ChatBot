from rest_framework import serializers
from .models import AIFeedModel
from django.contrib.auth.models import User

class AIFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIFeedModel
        fields = ['id','question','answer']
        extra_kwargs = {
            'answer': {'required': False}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        user.is_staff = True
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)