from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField


class Post(models.Model):
    # Reescreve o campo id padrão para ser um ShortUUID
    id = ShortUUIDField(primary_key=True, editable=False)

    # Adiciona um campo para o conteúdo do post com limitação de 140 caracteres como originalmente no Twitter
    content = models.TextField(max_length=140, blank=False, null=False)

    # Adiciona o timestamp de criação do post
    created_at = models.DateTimeField(auto_now_add=True)

    # Relaciona o post com o usuário que o criou, usando o modelo User do Django
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Adiciona um campo para marcar se o post foi editado ao menos uma vez
    edited = models.BooleanField(default=False)

    # Mantém uma lista de usuários que curtiram o post
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    # Relaciona um post a outro post, para criar uma thread de respostas
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    # Retorna a quantidade de curtidas que o post recebeu
    @property
    def likes(self):
        return self.liked_by.count()

    def __str__(self):
        return f"Post {self.id} by {self.created_by.username}"
