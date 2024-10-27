from django.apps import AppConfig

LOGIN_URL = 'main:login'

class FavoriteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'favorite'
