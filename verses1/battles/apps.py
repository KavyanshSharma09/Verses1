from django.apps import AppConfig


class BattlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'battles'

    def ready(self):
        # Import signal handlers
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
