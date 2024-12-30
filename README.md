# mini-twitter-api

## Sobre o Projeto

O mini-twitter-api é uma API REST simples que simula algumas funcionalidades básicas do Twitter/X.

Essa API possui endpoints que permitem ao usuário **criar** e **acessar** sua conta para que possa **ler**, **criar**, **editar**, **curtir** e **deletar** posts.

## Execução

### Guia para Uso da API

1. **Registro de Novo Usuário**
    - Endpoint: `/register/`
    - Método: `POST`
    - Descrição: Registre um novo usuário fornecendo os dados necessários.

2. **Login de Usuário Existente**
    - Endpoint: `/login/`
    - Método: `POST`
    - Descrição: Faça login com um usuário existente para obter o token de acesso JWT.

3. **Documentação da API**
    - Endpoint: `/docs/`
    - Descrição: Visite a documentação completa da API para explorar todos os endpoints disponíveis.

4. **Testes Usando a Interface Gráfica**
    - Acesse a documentação da API no endpoint `/docs/`.
    - Utilize a interface gráfica para testar os endpoints.
    - Para autenticação, insira o token JWT no formato: `Bearer <token>`.

Para mais detalhes, visite a [documentação da API](https://www.iflipe.pythonanywhere.com/docs/).

## Dependências

![Django Badge](https://img.shields.io/badge/Django-5.1.3-0e2f20?style=for-the-badge)
![DRF](https://img.shields.io/badge/DRF-3.15.2-a30000?style=for-the-badge)
![JWT](https://img.shields.io/badge/DRF--simplejwt-5.3.1-2980b9?style=for-the-badge)
![Swagger](https://img.shields.io/badge/drf--yasg-1.21.8-89bf04?style=for-the-badge)

## Documentação da API

A documentação da API pode ser encontrada [aqui](https://iflipe.pythonanywhere.com/docs/).

#### Desenvolvido por **[@iflipe](https://github.com/iflipe)**