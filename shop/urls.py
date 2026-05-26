from django.urls import path,include

from .views import all_products,add_product,my_cart,add_cart,minus_cart,delete_cart,create_checkout_session,create_order,stripe_cancel,stripe_success
app_name = 'shop'

urlpatterns = [
    path('add_product/', add_product,name='add_product'),
    path('my_cart/', my_cart,name='my_cart'),
    path('create_order/', create_order,name='create_order'),
    path('create_checkout_session/<int:order_id>/', create_checkout_session,name='create_checkout_session'),
    path('stripe/success/<int:order_id>/', stripe_success,name='stripe_success'),
    path('stripe/cancel/<int:order_id>/', stripe_cancel,name='stripe_cancel'),
    path('add_cart/<int:product_id>', add_cart,name='add_cart'),
    path('minus_cart/<int:product_id>', minus_cart,name='minus_cart'),
    path('delete_cart/<int:product_id>', delete_cart,name='delete_cart'),
    path('all_products/', all_products, name='all_products'),
    

]
