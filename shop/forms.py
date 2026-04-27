from django import forms

from .models import Product,Category

# class ProductForm(forms.Form):
#     title = forms.CharField(max_length=100, required=True,label='Title',widget=forms.TextInput(attrs={'class':'title'}))
#     description = forms.CharField(max_length=100)
#     stock_units = forms.IntegerField()
#     price = forms.DecimalField(max_digits=10,decimal_places=2)
#     seller_id = forms.IntegerField()
#     category_id = forms.IntegerField()
#     discount = forms.IntegerField()
    

class ProductForm(forms.ModelForm):
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
            raise forms.ValidationError('discount ниже 0')
        return data
