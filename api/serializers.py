from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "reply_to_id",
            "created_by",
            "edited",
            "likes",
            "created_at",
        ]
        read_only_fields = [
            "likes",
            "created_at",
            "created_by",
            "edited",
            "reply_to_id",
        ]

    def validate(self, value):
        post_id = self.context.get("reply_to_id")
        if not post_id:
            return value
        try:
            Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError("O post não existe.")
        return value

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        pk = self.context.get("reply_to_id")
        if pk:
            validated_data["reply_to_id"] = int(pk)
        return Post.objects.create(**validated_data)


class PostDetailSerializer(ModelSerializer):
    replies = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "reply_to",
            "created_by",
            "edited",
            "likes",
            "created_at",
            "replies",
        ]
        read_only_fields = [
            "likes",
            "created_at",
            "created_by",
            "replies",
            "reply_to",
            "edited",
        ]

    def update(self, instance, validated_data):
        validated_data["edited"] = True
        return super().update(instance, validated_data)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
