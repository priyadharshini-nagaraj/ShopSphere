from django.shortcuts import render,redirect
from .models import ProductModel,CartModel
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        cart_count = CartModel.objects.filter(host = request.user).count()
    else:
        cart_count = 0
    trending = False
    offer = False
    if 'q' in request.GET:
        q = request.GET['q']
        all_products = ProductModel.objects.filter(Q(pname__icontains = q) | Q(pcategory__icontains = q) & Q(is_delete = False))
        if len(all_products) == 0:
            messages.error(request, 'NO PRODUCTS !!!')
    elif 'cat' in request.GET:
        cat = request.GET['cat']
        all_products = ProductModel.objects.filter(pcategory = cat)
    elif 'offer' in request.GET:
        all_products = ProductModel.objects.filter(Q(offer = True) & Q(is_delete = False))
        offer = True
    elif 'trending' in request.GET:
        all_products = ProductModel.objects.filter(Q(trending = True) & Q(is_delete = False))
        trending = True
    else:
        all_products = ProductModel.objects.all()
    category = []
    for i in ProductModel.objects.all():
        if i.pcategory not in category:
            category.append(i.pcategory)

    return render(request,'home.html',{'all_products': all_products, 'category': category,'trending': trending, 'offer': offer,'home_nav':True,'cart_count': cart_count})

@login_required
def cart(request):
    cart_count = CartModel.objects.filter(host = request.user).count()
    cart_product = CartModel.objects.filter(host = request.user)
    TA=0
    for i in cart_product:
        TA+=i.total_price
    return render(request,'cart.html',{'cart_product':cart_product, 'TA':TA,'cart_count':cart_count})

@login_required
def addcart(request,pk):
    product = ProductModel.objects.get(id = pk)
    try:
        cp = CartModel.objects.get(pname = product.pname,host=request.user)
        cp.quantity+=1
        cp.total_price+=product.price
        cp.save()
        return redirect(cart)
    except:
        CartModel.objects.create(
            pname = product.pname,
            pcategory = product.pcategory,
            price = product.price,
            total_price = product.price,
            host = request.user
        )
        return redirect('home')

def remove(request,pk):
    data = CartModel.objects.get(id=pk,host=request.user).delete()
    return redirect(cart)

def plus(request,pk):
    data = CartModel.objects.get(id=pk,host=request.user)
    data.quantity+=1
    data.total_price+=data.price
    data.save()
    return redirect(cart)

def minus(request,pk):
    data = CartModel.objects.get(id=pk,host=request.user)
    if data.quantity >1:
        data.quantity-=1
        data.total_price-=data.price
        data.save()
        return redirect('cart')
    else:
        data.delete()
        return redirect('cart')