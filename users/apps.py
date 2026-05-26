from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        from apscheduler.schedulers.background import BackgroundScheduler
        from .user_utils import delete_expired_user

        scheduler = BackgroundScheduler()
        scheduler.add_job(delete_expired_user,'interval',minutes=15)
        scheduler.start()