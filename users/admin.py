from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    model = Seller
    list_display=('user',)
@admin.register(CustomerUser)
class CategoryAdmin(admin.ModelAdmin):
    model = CustomerUser
    list_display=('username','role','phone_number','email',)
    list_editable = ('role','email',)