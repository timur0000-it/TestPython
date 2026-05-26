from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model


def delete_expired_user():
    time_to_delete = timezone.now() - timedelta(minutes=15)
    User=get_user_model()
    dead_users = User.objects.filter(is_active = False,date_joined__lt=time_to_delete)
    delete_count,details = dead_users.delete()
    if delete_count > 0:
        print(f'Удалено {delete_count} неактивных пользователей')