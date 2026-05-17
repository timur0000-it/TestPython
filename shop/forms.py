from django import forms

from .models import Product,Category,Cart,ProductImages


    

class ProductForm(forms.ModelForm):
    image_field = forms.ImageField(required=False)
    class Meta:
        model = Product
        exclude = ['seller_id']

        
    def clean(self):
        data = self.cleaned_data
        price = self.cleaned_data['price']
        stock_units = self.cleaned_data['stock_units']
        discount = self.cleaned_data['discount']
        if price < 0:
            raise forms.ValidationError('Цена ниже 0')
        if stock_units < 0:
            raise forms.ValidationError('stock_units ниже 0')
        if discount >= 101:
            raise forms.ValidationError('discount больше 100')
        return data
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        exclude = ['user_id']