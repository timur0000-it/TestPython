from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail
from django.db import transaction

@receiver(post_save,sender=CustomerUser)
def check_registration(sender,instance,created,**kwargs):
    if created:
        obj,raw_code = ActivationCode.create_for_user(instance)
        def _after_comit_send():
            subject = 'Код подтверждения регистрации'
            message = f"""
            Привет,{instance.username}!
            Код подтверждения: {raw_code}
            Действителен 15 минут
            """
            try:
                send_mail(subject,message,None,[instance.email])
            except:
                pass
        transaction.on_commit(_after_comit_send)
