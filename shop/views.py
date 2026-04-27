# GLOBAL
from django.shortcuts import render,redirect
# LOCAL
from .models import Product,Category
from .forms import ProductForm
from users.models import CustomerUser,Seller

def add_product(request):
    if request.method =='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller_id = Seller.objects.get(user=request.user)
            product.save()
            return redirect('shop:all_products')
        else:
            print(form.errors)
        return render(request,'add_product.html',{'form':form,'errors':form.errors})
 
    else:
        form = ProductForm()
    return render(request,'add_product.html',{'form':form})

def all_products(request):
    if request.method =='POST':
            # Перенаправление
        return redirect('shop:all_products')
    else:
        all_products = Product.objects.all()
    return render(request,'all_products.html',{'all_products':all_products})

