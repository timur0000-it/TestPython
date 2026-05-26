# GLOBAL
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import stripe
# LOCAL
from .models import Product,Category,Cart,ProductImages,Order
from .forms import ProductForm,CartForm
from users.models import CustomerUser,Seller
from users.views import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def add_product(request):
    if request.user.is_customer() or request.user == None:
        messages.warning(request, 'Только для продавцов')
        return redirect('users:signin')
    if request.method =='POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller_id = Seller.objects.get(user=request.user)
            product.save()
            if form.cleaned_data.get('image_field')!=None:
                ProductImages.objects.create(product_id=product,is_main=True,image=form.cleaned_data.get('image_field'))
                return redirect('shop:all_products')
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

@login_required
def create_order(request):
    user = request.user
    cart_items  = Cart.objects.filter(user_id=request.user)
    if not cart_items.exists():
        return redirect('shop:my_cart')
    total_amount:int = 0 
    for i in cart_items:
        total_amount+= i.total_price()
    order = Order.objects.create(user=user,email=user.email,total_amount=total_amount)
    return redirect('shop:create_checkout_session',order_id=order.id)

def create_checkout_session(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    line_item = {
        'price_data':{
            'currency':'kzt',
            'unit_amount':int(order.total_amount * 100),
            'product_data':{
            'name': f'Заказ  №{order.id}'
        }
        },
        
        'quantity':1
    }
    cancel_url = request.build_absolute_uri(reverse('shop:stripe_cancel',args=[order.id]))
    succces_url = request.build_absolute_uri(reverse('shop:stripe_success',args=[order.id]))
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[line_item],
            mode='payment',
            success_url = succces_url,
            cancel_url = cancel_url
        )
        order.stripe_id = checkout_session.id
        order.save()
        return redirect(checkout_session.url,code = 303)
    except Exception as e:
        print(e)
        return redirect('shop:my_cart')

def stripe_success(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    session_id = order.stripe_id
    if not session_id:
        messages.error(request, 'Stripe session not found')
        return redirect('shop:my_cart')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            order.status = 'paid'
            Cart.objects.filter(user_id=order.user).delete()
            order.save()
            messages.success(request, 'Payment successful')
            return redirect('shop:all_products')
        else:
            messages.warning(request, 'Payment not completed')
            return redirect('shop:my_cart')
    except Exception as e:
        print(e)
        messages.error(request, 'Stripe error')
        return redirect('shop:my_cart')
    
def stripe_cancel(request,order_id):
    order = get_object_or_404(Order,id=order_id)
# сбросить статус заказа
    session_id = order.stripe_id
    if not session_id:
        messages.error(request, 'Stripe session not found')
        return redirect('shop:my_cart')
    else:
        order.status = 'created'
        order.save()
        messages.info(request, 'Payment canceled')
        return redirect('shop:all_products') 