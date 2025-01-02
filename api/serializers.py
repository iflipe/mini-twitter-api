from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class PostSerializer(HyperlinkedModelSerializer):
    # Retorna o nome do usuário que criou o post
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            "content",
            "reply_to",
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
            "reply_to",
        ]
        extra_kwargs = {
            "url": {"view_name": "post-detail"},
        }

    def validate(self, value):
        """
        Valida se o post ao qual o usuário está respondendo existe.
        """
        post_id = self.context.get("reply_to")
        if not post_id:
            return value
        try:
            Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError("O post não existe.")
        return value

    def create(self, validated_data):
        """
        Adiciona o usuário autenticado como criador do post e, se o post for uma resposta, adiciona o post ao qual está respondendo.
        """
        validated_data["created_by"] = self.context["request"].user
        pk = self.context.get("reply_to_id")
        if pk:
            validated_data["reply_to_id"] = str(pk)
        return Post.objects.create(**validated_data)


class PostDetailSerializer(HyperlinkedModelSerializer):
    # Retorna o nome do usuário que criou o post
    created_by = serializers.ReadOnlyField(source="created_by.username")
    replies = serializers.HyperlinkedRelatedField(
        view_name="post-detail",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "url",
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
        extra_kwargs = {
            "url": {"view_name": "post-detail"},
        }

    def update(self, instance, validated_data):
        """
        Atualiza o post e o marca como editado.
        """
        validated_data["edited"] = True
        return super().update(instance, validated_data)


class LikePostSerializer(HyperlinkedModelSerializer):
    # Retorna o nome do usuário que criou o post
    created_by = serializers.ReadOnlyField(source="created_by.username")
    replies = serializers.HyperlinkedRelatedField(
        view_name="post-detail",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "url",
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
            "content",
            "created_by",
            "replies",
            "reply_to",
            "edited",
        ]

    def update(self, instance, validated_data):
        """
        Atualiza o post para ser curtido ou descurtido pelo usuário atual.
        Se a ação do contexto for "like" e o método da requisição for "POST", o usuário atual é adicionado ao campo liked_by do post.
        Se a ação do contexto for "like" e o método da requisição for "DELETE", o usuário atual é removido do campo liked_by do post.
        """

        if (
            self.context.get("action") == "like"
            and self.context["request"].method == "POST"
        ):
            instance.liked_by.add(self.context["request"].user)
        if (
            self.context.get("action") == "like"
            and self.context["request"].method == "DELETE"
        ):
            instance.liked_by.remove(self.context["request"].user)
        return instance


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "username", "password"]

        # Adiciona estilo para ocultar a senha na versão navegável da API.
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        try:
            validate_password(validated_data["password"], user=user)
        except ValidationError as e:
            raise e

        user.save()
        return user
