from django.db import models
from users.models import CustomerUser,Seller
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    # Наследование от самого себя
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.category_name

class Product(models.Model):
    title = models.CharField(max_length=150)
    category_id = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    description =models.TextField()
    stock_units = models.PositiveBigIntegerField(default=0)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    seller_id = models.ForeignKey(Seller,on_delete=models.CASCADE)
    discount = models.PositiveBigIntegerField(default=0)
    
    
    @property
    def is_available(self):
        if_in_stock = self.stock_units > 0
        return if_in_stock
        
    
    def __str__(self):
        return self.title

class ProductImages(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'Products/')
    is_main = models.BooleanField(default=False)
    


class Cart(models.Model):
    user_id = models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_price(self):
        return(self.product_id.price - (self.product_id.price*self.product_id.discount)/100) * self.quantity 
    
        
    
    def __str__(self):
        return f'{self.user_id.username} - {self.product_id.title} x {self.quantity}'

    
