from django.apps import AppConfig


class BattlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'battles'

    def ready(self):
        try:
            from . import signals  
        except Exception:
            pass

        # Start the self-ping keep-alive thread on Render (prevents cold starts)
        from .keep_alive import start as start_keep_alive
        start_keep_alive()
