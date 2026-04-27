from django.urls import path,include

from .views import all_products,add_product
app_name = 'shop'

urlpatterns = [
    path('add_product/', add_product,name='add_product'),
    path('all_products/', all_products, name='all_products')
    

]
