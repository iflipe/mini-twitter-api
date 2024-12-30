from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Retorna um dicionário com os tokens de acesso e refresh para um usuário
    """
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
