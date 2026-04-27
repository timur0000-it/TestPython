from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomerUser(AbstractUser):
    photo = models.ImageField(blank=True,null=True,help_text='Фото профиля (рекомендуемые размер 400x400)',upload_to='user_photos/')
    USER_ROLES = (('customer','Покупатель'),
                  ('seller',"Продавец"))
    role = models.CharField(max_length=20,choices=USER_ROLES, default='customer')
    phone_number = models.CharField(max_length=32,blank=False,null=False)
    parol= models.CharField(max_length=5,blank=True,null=True)
    def is_customer(self):
        return self.role == 'customer'
    
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

    # статические файлы и медиа файлы
    # статические файлы - это то что необходимо для проекта (css,js,иконки)
    # медиа файлы - это файлы которые грузятся пользователем или извне
