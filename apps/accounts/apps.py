from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "apps.accounts"  # Caminho completo
    label = "accounts"  # Usado em AUTH_USER_MODEL
