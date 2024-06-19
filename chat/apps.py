from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    #\ def ready(self):
    #     # Importing signals to ensure signal handlers are registered
    #     from . import signals
