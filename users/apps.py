from django.apps import AppConfig
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        super().ready()  # Ensures parent class initialization
        import users.signals  # This imports the signals module to register signal handlers