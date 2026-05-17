# GLOBAL
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# LOCAL
from .models import Product,Category,Cart,ProductImages
from .forms import ProductForm,CartForm
from users.models import CustomerUser,Seller
from users.views import login_required

@login_required
def add_product(request):
    if request.method =='POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller_id = Seller.objects.get(user=request.user)
            product.save()
            if form.cleaned_data.get('image_field')!=None:
                ProductImages.objects.create(product_id=product,is_main=True,image=form.cleaned_data.get('image_field'))
                return redirect('shop:all_products')
        else:
            print(form.errors)
        return render(request,'add_product.html',{'form':form})
 
    else:
        form = ProductForm()
    return render(request,'add_product.html',{'form':form})

def testt():
    print('Hello World')

@login_required
def all_products(request):
    my_products = Cart.objects.filter(user_id=request.user)
    if request.method =='POST':
        title = request.POST.get('title').strip()
        all_products = Product.objects.filter(title__icontains=title)
        all_images=ProductImages.objects.filter(is_main=True)
    else:
        
        all_products = Product.objects.all()
        all_images=ProductImages.objects.filter(is_main=True)
    return render(request,'all_products.html',{'all_products':all_products,'all_images':all_images,'my_products':my_products})

@login_required
def my_cart(request):
    my_products = Cart.objects.filter(user_id=request.user)
    money=0
    for i in my_products:
        money+=i.total_price()
    return render(request,'my_cart.html',{'my_products':my_products,'money':money})


@login_required
@require_POST
def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    cart = Cart.objects.filter(user_id=request.user,product_id=product).first()
    if cart !=None:
        cart.quantity+=1
        cart.save()
        return JsonResponse({'status': 'ok', 'product_id': product_id,'qua':cart.quantity})
    else:
        cart = Cart.objects.create(user_id=request.user,product_id=product)
        return JsonResponse({'status': 'ok', 'product_id': product_id,'qua':cart.quantity})

@login_required
def minus_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    cart = Cart.objects.filter(user_id=request.user,product_id=product).first()
    if cart.quantity==1:
        cart.delete()
        return JsonResponse({'status': 'not', 'product_id': product_id})
    if cart !=None:
        cart.quantity-=1
        cart.save()
        return JsonResponse({'status': 'not', 'product_id': product_id,'qua':cart.quantity})
    

@login_required
def delete_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    cart = Cart.objects.filter(user_id=request.user,product_id=product).first()
    cart.delete()
    return redirect('shop:my_cart')

