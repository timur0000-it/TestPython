from django.urls import path,include

from .views import all_products,add_product,my_cart,add_cart,minus_cart,delete_cart
app_name = 'shop'

urlpatterns = [
    path('add_product/', add_product,name='add_product'),
    path('my_cart/', my_cart,name='my_cart'),
    path('add_cart/<int:product_id>', add_cart,name='add_cart'),
    path('minus_cart/<int:product_id>', minus_cart,name='minus_cart'),
    path('delete_cart/<int:product_id>', delete_cart,name='delete_cart'),
    path('all_products/', all_products, name='all_products'),
    

]
