from django.shortcuts import render, redirect
from app_version1.models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerprofileForm
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def home(request):
    topwear = Product.objects.filter(category='TW')
    bottomwear = Product.objects.filter(category='BW')
    mobile = Product.objects.filter(category='M')
    laptop = Product.objects.filter(category='L')
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    context={
        'topwear': topwear,
        'bottomwear': bottomwear,
        'mobile': mobile,
        'laptop': laptop,
        'totalitem': totalitem,
    } 

    return render(request, 'app/home.html', context)

def search(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if request.method == 'GET':
        find = request.GET.get('find')
        search = Product.objects.filter(title__contains=find)
    context={
        'search': search,
        'totalitem': totalitem,
        'find': find,
    }
    return render(request, 'app/search.html', context)


def product_detail(request, p_id):
    totalitem = 0
    product_id = Product.objects.get(id=p_id)
    item_in_cart = False
    if request.user.is_authenticated:
        item_in_cart = Cart.objects.filter(Q(product=product_id) & Q(user=request.user)).exists()
        totalitem = len(Cart.objects.filter(user=request.user))
    context={
        'product_id': product_id,
        'item_in_cart': item_in_cart,
        'totalitem': totalitem,
    }

    return render(request, 'app/productdetail.html', context)

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('id')
    product = Product.objects.get(id=product_id)
    my_data = Cart(user=user, product=product)
    my_data.save()
    return redirect('show-to-cart')

@login_required
def show_to_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        Shipping = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user ]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + Shipping
        context={
            'cart': cart,
            'amount': amount,
            'Shipping': Shipping,
            'total_amount': total_amount,
            'totalitem': totalitem,
        }
        return render(request, 'app/addtocart.html', context)

@login_required    
def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity += 1
        cart.save()
        amount = 0.0
        Shipping = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + Shipping
        data={
            'quantity': cart.quantity,
            'amount': amount,
            'total_amount': total_amount,
        }
        return JsonResponse(data)

@login_required    
def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity -= 1
        if cart.quantity < 1:
            cart.quantity = 1
        cart.save()
        amount = 0.0
        Shipping = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + Shipping
        data={
            'quantity': cart.quantity,
            'amount': amount,
            'total_amount': total_amount,
        }
        return JsonResponse(data)  

@login_required
def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.delete()
        amount = 0.0
        Shipping = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + Shipping
        data={
            'amount': amount,
            'total_amount': total_amount,
        }
        return JsonResponse(data)         


def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def profile(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        form = CustomerprofileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            my_data = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            my_data.save()
            messages.success(request, 'Congratulations!! Profile Upadted Successfully')
            return redirect('profile') 
    else:
        form = CustomerprofileForm()
    context={
        'form': form,
        'active': 'btn-primary',
        'totalitem': totalitem, 
    }        
    return render(request, 'app/profile.html', context)

@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    my_data = Customer.objects.filter(user=request.user)
    context={
        'my_data': my_data,
        'active': 'btn-primary',
        'totalitem': totalitem, 
    } 
    return render(request, 'app/address.html', context)


def mobile(request, data=None):
    totalitem = 0
    btn = ''
    btn1s = ''
    btn1v = ''
    btn1a = ''
    btn2 = ''
    btn3 = ''
    btn4 = ''
    active = 'active'
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category='M')
        btn = 'active'
    elif data == 'Samsung' or data == 'Vivo' or data == 'Apple':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
        if data == 'Samsung':
            btn1s = 'active'
        elif data == 'Vivo':
            btn1v = 'active'
        elif data == 'Apple':
            btn1a = 'active'
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
        btn2 = 'active'
    elif data == 'between':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__range=(10000, 20000))   
        btn3 = 'active'    
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)   
        btn4 = 'active'    
    context={
        'mobiles': mobiles,
        'totalitem': totalitem,
        'btn': btn,
        'btn1s': btn1s,
        'btn1v': btn1v,
        'btn1a': btn1a,
        'btn2': btn2,
        'btn3': btn3,
        'btn4': btn4,
        'active': active,
    }    
    return render(request, 'app/mobile.html', context)


def laptop(request, data=None):
    totalitem = 0
    btn = ''
    btn1s = ''
    btn1v = ''
    btn1a = ''
    btn2 = ''
    btn3 = ''
    btn4 = ''
    active = 'active'
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptops = Product.objects.filter(category='L')
        btn = 'active'
    elif data == 'Apple' or data == 'HP' or data == 'Lenovo':
        laptops = Product.objects.filter(category='L').filter(brand=data)
        if data == 'Apple':
            btn1s = 'active'
        elif data == 'HP':
            btn1v = 'active'
        elif data == 'Lenovo':
            btn1a = 'active'
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=10000)
        btn2 = 'active' 
    elif data == 'between':
        laptops = Product.objects.filter(category='L').filter(discounted_price__range=(10000, 20000)) 
        btn3 = 'active'      
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=20000)
        btn4 = 'active'       
    context={
        'laptops': laptops,
        'totalitem': totalitem,
        'btn': btn,
        'btn1s': btn1s,
        'btn1v': btn1v,
        'btn1a': btn1a,
        'btn2': btn2,
        'btn3': btn3,
        'btn4': btn4,
        'active': active,
    } 
    return render(request, 'app/laptop.html', context)

def topwear(request, data=None):
    totalitem = 0
    btn = ''
    btn1s = ''
    btn1v = ''
    btn1a = ''
    btn2 = ''
    btn3 = ''
    btn4 = ''
    active1 = 'active'
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        topwears = Product.objects.filter(category='TW')
        btn = 'active'
    elif data == 'Almuda' or data == 'Wrogn' or data == 'Smartees':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
        if data == 'Almuda':
            btn1s = 'active'
        elif data == 'Wrogn':
            btn1v = 'active'
        elif data == 'Smartees':
            btn1a = 'active'
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=10000)
        btn2 = 'active'
    elif data == 'between':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__range=(10000, 20000)) 
        btn3 = 'active'      
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=20000) 
        btn4 = 'active'      
    context={
        'topwears': topwears,
        'totalitem': totalitem,
        'btn': btn,
        'btn1s': btn1s,
        'btn1v': btn1v,
        'btn1a': btn1a,
        'btn2': btn2,
        'btn3': btn3,
        'btn4': btn4,
        'active1': active1,
    } 
    return render(request, 'app/topwear.html', context)

def bottomwear(request, data=None):
    totalitem = 0
    btn = ''
    btn1s = ''
    btn1v = ''
    btn1a = ''
    btn2 = ''
    btn3 = ''
    btn4 = ''
    active1 = 'active'
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        bottomwear = Product.objects.filter(category='BW')
        btn = 'active'
    elif data == 'Akacy' or data == 'Podge' or data == 'Tyffan':
        bottomwear = Product.objects.filter(category='BW').filter(brand=data)
        if data == 'Akacy':
            btn1s = 'active'
        elif data == 'Podge':
            btn1v = 'active'
        elif data == 'Tyffan':
            btn1a = 'active'
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=10000)
        btn2 = 'active'
    elif data == 'between':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__range=(10000, 20000))  
        btn3 = 'active'     
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt=20000) 
        btn4 = 'active'      
    context={
        'bottomwear': bottomwear,
        'totalitem': totalitem,
        'btn': btn,
        'btn1s': btn1s,
        'btn1v': btn1v,
        'btn1a': btn1a,
        'btn2': btn2,
        'btn3': btn3,
        'btn4': btn4,
        'active1': active1,
    } 
    return render(request, 'app/bottomwear.html', context)


def customerregistration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST, auto_id=True)
        if form.is_valid(): 
            print(form.cleaned_data['username'])
            print(form.cleaned_data['email'])
            print(form.cleaned_data['password1'])
            print(form.cleaned_data['password2'])
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    context={
        'form': form,
    } 
    return render(request, 'app/customerregistration.html', context)

@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    Shipping = 50.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + Shipping
    context={
        'add': add,
        'total_amount': total_amount,
        'cart_items': cart_items,
        'totalitem': totalitem,
    } 
    return render(request, 'app/checkout.html', context)

@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,Customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    my_data = OrderPlaced.objects.filter(user=request.user)
    context={
        'my_data': my_data,
        'totalitem': totalitem,
    }
    return render(request, 'app/orders.html', context)


