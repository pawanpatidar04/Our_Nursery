from unicodedata import category
from django.shortcuts import render
from .models import Contact, User, ProductCart
from nurseryapp.models import Contact,Product
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import transaction
from django.core.mail import send_mail
import random
from django.conf import settings

def index(request):
    latest_product = Product.objects.order_by('-id')[:6]
    return render(request,"index.html", {'Product': latest_product})

def Signup(request):
    return render(request, "signup.html" )

def handlesignup(request):
    if request.method != 'POST':
        pass
    else:
        global u_name, email, password,confirm_password, role_id
        u_name=request.POST['name']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        role=request.POST['role']
        role_id = 0
        if(role=='seller'):
            role_id=1

            
        random1 = random.randint(1000, 9999)
        request.session['random1'] = random1
        print(u_name, random1)

        if password != confirm_password:
           messages.warning(request,"password is not matching")
           return render(request,'signup.html')

        send_mail(
            'Nursery',
            f'Your OTP for register with  is :{random1}',
            settings.EMAIL_HOST_USER, 
            [email],
            fail_silently=False,
        )
        return HttpResponseRedirect('/verify_otp')
        # return HttpResponseRedirect('index.html')
    return render(request, "login.html" )

def Login(request):
    return render(request, "login.html" )

def read_services(request):
    return render(request,"read_services.html")

def Book_now(request):
    return render(request,"book_now.html")



def opt_page(request):
    return render(request, "verify_otp.html" )

def confirm_otp(request):
    if request.method != 'POST':
        pass
    else:
        user_otp = request.POST.get('otp')
        print(user_otp)
        
        random1 = request.session.get('random1')

        print(random1)
        if(random1 == int(user_otp)):
            print('Register Successfully')
            
            newuser = User()
            newuser.name = u_name
            newuser.email = email
            newuser.password = password
            newuser.role = role_id
            newuser.save()

            return HttpResponseRedirect('/login/')

        else:
            messages.error(request, 'otp does not match')    
            print('not match')
    return render(request, 'verify_otp.html')
    
def handlelogin(request):
    if request.method != 'POST':
        pass
    else:
        email=request.POST['email']
        password=request.POST['pass1']

        queryset = User.objects.filter(email= email, password=password)
        list(queryset)
        if(len(queryset) != 0):    
            print('loged in successfully')
            user = User.objects.get(email = email)
            request.session['email'] = email
            request.session['role'] = user.role
            # request.session['role'] = email
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Email and password does not match')    
    return render(request, "login.html" )

def handlelogout(request):
    request.session.flush()
    return HttpResponseRedirect('/')

def showproduct(request):
    Productdata=Product.objects.all()
    print(Productdata)
    return render(request,'show-products.html',{'Product':Productdata})

def AddContact(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        number=request.POST["number"]
        message=request.POST["message"]
   
        myquery= Contact(name=name,email=email,number=number,message=message)
        myquery.save()
        # return HttpResponse(request, "Thanks for contact  us")
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def services(request):
    return render(request,"services.html")

def categrise(request):
    return render(request,"categrise.html")

def product(request):
    return render(request,"product.html")

def deal(request):
    return render(request,"deal.html")

#seller functions

def sellerDashboard(request):
    currentUser = request.session.get('email')
    createseller = User.objects.get(email=currentUser)
    products = Product.objects.filter(seller=createseller)
    print(products)
    return render(request,"seller-dashboard.html", {'Product':products})

def AddProductForm(request):
    return render(request,"add-product.html")

def MyCart(request):
    currentUser = request.session.get('email')
    user = User.objects.get(email=currentUser)
    
    getproductsID = ProductCart.objects.filter(
        user_id = user.id
    )
    allproducts = []
    total_price = 0
    total_product = 0
    for p in getproductsID:
        getproduct = Product.objects.get(id=p.product_id)
        dicproduct = {
            "qunatity": p.qunatity,
            "product_id": p.product_id,
            "image": getproduct.image,
            "name": getproduct.product_name,
            "price": getproduct.price,
            "category": getproduct.category
        }
        total_product = total_product + 1
        total_price = total_price + (getproduct.price * p.qunatity)
        allproducts.append(dicproduct)

    return render(request,"my-cart.html", {'Product': allproducts,  'TotalPrice': total_price, 'NoOfProduct': total_product})

def RemoveCart(request, product_id):
    with transaction.atomic():
        cartItem = ProductCart.objects.filter(product_id = product_id)
        cartItem.delete()
    return HttpResponseRedirect('/mycart')


def CreatProduct(request):
    name=request.POST['name']
    price=request.POST['price']
    image=request.POST['image']
    desc=request.POST['details']
    category=request.POST['category']

    currentUser = request.session.get('email')

    createseller = User.objects.get(email=currentUser)
    print(name, image, price, desc)
    newproduct=Product(
        product_name=name,
        price=price,
        image=image,
        category=category,
        desc=desc,
        seller=createseller,
    )
    newproduct.save()
    return render(request,"seller-dashboard.html")


def categoy_products(request, category):
    # categoryname = request.GET.get('category')
    products = Product.objects.filter(category=category)
    return render(request,"category-product.html", {'Product':products})

def addCart(request):
    if(request.session.get('email')):
        id = request.POST['id']
        qunatity = request.POST['quntity']
        print(id, qunatity)
        email = request.session.get('email')
        poduct = Product.objects.get(id=id)
        user = User.objects.get(email=email)
        newproduct = ProductCart()
        newproduct.user = user
        newproduct.product = poduct
        newproduct.qunatity = request.POST['quntity']
        newproduct.save()
        return HttpResponseRedirect('/mycart')
    else:
        return HttpResponseRedirect('/login')



def Search(request):
    search_query = request.POST['query']
    products = Product.objects.filter(product_name__icontains=search_query)
    return render(request, "search-result.html", {'Product':products})

def deleteproduct(request, product_id):
    Item = Product.objects.filter(id = product_id)
    Item.delete()
    return HttpResponseRedirect('/dashboard')

    