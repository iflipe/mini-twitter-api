from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post


class PostSerializer(ModelSerializer):
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
        ]
        read_only_fields = ["likes", "created_at", "created_by", "edited"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
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
