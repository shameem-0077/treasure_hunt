from django.apps import AppConfig


class HuntsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hunts'

    def ready(self):
        import hunts.signals
