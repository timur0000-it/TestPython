from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta 
import random
# Create your models here.

class CustomerUser(AbstractUser):
    photo = models.ImageField(blank=True,null=True,help_text='Фото профиля (рекомендуемые размер 400x400)',upload_to='user_photos/')
    USER_ROLES = (('customer','Покупатель'),
                  ('seller',"Продавец"))
    role = models.CharField(max_length=20,choices=USER_ROLES, default='customer')
    phone_number = models.CharField(max_length=32,blank=False,null=False)

    def is_customer(self):
        return self.role == 'customer'
    @property
    def is_seller(self):
        return self.role == 'seller'
    
    def __str__(self):
        return self.username

class Seller(models.Model):
    user = models.OneToOneField(CustomerUser,on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3,decimal_places=2,default=0.0) 
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    
    def __str__(self):
        return self.user.username
class ActivationCode(models.Model):
    user = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,related_name='activation_codes')
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    expiers_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    attemps = models.PositiveBigIntegerField(default=0)

    @classmethod
    def random_code(cls):
        raw_code=str(random.randint(1000,9999))
        return raw_code
    
    @classmethod
    def create_for_user(cls,user,lifetime_minutes = 15):
        raw_code = cls.random_code()
        obj = cls.objects.create(
            user=user,
            code=raw_code,
            expiers_at = timezone.now() + timedelta(minutes=lifetime_minutes)
        )
        return obj,raw_code
    
    def check_code(self,code,max_attemps=5):
        if self.used:
            return False, 'код использован'
        if timezone.now() > self.expiers_at:
            self.delete()
            return False, 'Время и стекло'
        if self.attemps>max_attemps:
            self.delete()
            return False, 'кол-во попыток превышает норму'
        if code == self.code:
            self.used=True
            self.save()
            return True,None
        self.attemps+=1
        self.save()
        return False,'Неверный код'

    # статические файлы и медиа файлы
    # статические файлы - это то что необходимо для проекта (css,js,иконки)
    # медиа файлы - это файлы которые грузятся пользователем или извне
