from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.core.mail import send_mail
from ecommerceApp.models import Products, Cart, Order
from django.contrib import messages
# Create your views here.

# Home Function
def index(request):
    products = Products.objects.all()
    return render(request , 'home.html' ,{'products': products} )
# signup function
def signup(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            ver_code = random.randint(1000, 9999)
            from_email = 'ex@ansqazzafi.com'
            subject = 'Registration Confirmation'
            message = f'Thank you for registering with us! Your verification code is: {ver_code}'
            recipient_list = [email]

            if password != cpassword:
                return HttpResponse("Passwords didn't match")
            elif User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists. Please choose a different one.")
            else:
                send_mail(subject, message, from_email, recipient_list)
                request.session['ver'] = ver_code
                request.session['user'] = username
                request.session['email'] = email
                request.session['password'] = password
                return redirect('/verification')
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred while processing your request.")
    return render(request, 'signup.html')
# signin function
def signin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request , username=username , password=password)
            print(user)
            if user is not None:
                login(request , user)
                return redirect('/')
            else:
                return HttpResponse("Invalid user and password")
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred while processing your request.")
    return render(request , 'signin.html')
# Verification Function
def verification(request):
    if request.method == 'POST':
        try:
            Uverification_code = request.POST.get('verification_code')
            ver_code = request.session.get('ver')
            username = request.session.get('user')
            email = request.session.get('email')
            password = request.session.get('password')
            if Uverification_code == str(ver_code):
                user = User.objects.create_user(username , email , password)
                user.save()
                print("user added success")
                return redirect('/signin')
            else:
                print("invalid")
                return redirect('/verification')
        except Exception as e:
            print("An error occurred:", e)
            return redirect('/verification')

    return render(request, 'verification.html')
# Logout Function
def logout_user(request):
    logout(request)
    return redirect('/')

def productpage(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    user = request.user
    if request.method == 'POST':
            quantity_str = request.POST.get('quantity')
            if quantity_str is None:
                return HttpResponse("Quantity is required")
            try:
                quantity = int(quantity_str)
            except ValueError:
                return HttpResponse("Invalid quantity")
            if quantity <= 0:
                return HttpResponse("Quantity must be a positive integer")
            if product.stock is not None:
                if quantity <= product.stock:
                    product = Products.objects.select_for_update().get(product_id=product_id)
                    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
                    cart_item.quantity += quantity
                    cart_item.price = product.price * cart_item.quantity
                    cart_item.save()
                    messages.success(request , "Item added into the Cart")
                else:
                    return HttpResponse("Quantity exceeds available stock")
            else:
                return HttpResponse("Stock not available right now")
    return render(request, 'productpage.html', {'product': product})

def viewCart(request):
    user = request.user
    if user.is_anonymous:
        return redirect('/signin')
    else:
        cartItem = Cart.objects.filter(user=user)
    return render(request , 'cart.html' , {'cartItem':cartItem})

def deleteCart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.delete()
    messages.success(request , "Item Deleted From Cart sucessfully")
    return redirect('/cart')

def checkout(request, id):
    item = Cart.objects.get(id=id)
    product = item.product
    quantity1 = item.quantity
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        cart = item
        total_price = item.price
        if quantity1 > product.stock:
            return HttpResponse("Stock not available")
        else:
            checkoutItem = Order.objects.create(name=name, email=email, address=address, phone_number=phone_number ,total_price=total_price, cart=cart)
            product.stock -= quantity1
            checkoutItem.save()
            product.save()
            return render(request, 'checkout.html', {'item': item}) 
    return render(request, 'checkout.html', {'item': item})


def u_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(name=request.user)
        return render(request, 'user_orders.html', {'orders': orders})
    else:
        return HttpResponse("Oops 404")


def search(request):
    if request.method == "GET":
        search_query = request.GET.get("search")
        if search_query:
            allproducts = Products.objects.filter(name__contains=search_query) 
            print(allproducts)
            return render(request, 'search.html', {'allproducts': allproducts})
        else:
            return render(request, 'search.html', {})
    return render(request , 'search.html')


# def deleteorder(request , id):
#     order = Order.objects.get(id=id)
#     order.delete()
#     return render(request , 'user_orders.html')