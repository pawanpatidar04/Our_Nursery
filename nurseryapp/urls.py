from django.urls import path
from nurseryapp import views
from .import views

urlpatterns = [
    #handle user session (Login, Signup, Logout)
    path('signup/',views.Signup,name='signup'),
    path('login/',views.Login,name='login'),
    path('handlelogin/',views.handlelogin,name='handlelogin'),
    path('handlesignup/',views.handlesignup,name='handlesignup'),
    path('logout/',views.handlelogout,name='handlelogout'),


    path('',views.index,name="index.html"),
    path('categrise',views.categrise,name="categrise"),
    path('services',views.services,name="services"),
    path('deal',views.deal,name="deal"),
    path('contact',views.AddContact,name="contact.html"),
    path('about',views.about,name="about.html"),
    path('product',views.product,name="product.html"),
    path('show-product/',views.showproduct,name=''),

    path('search/',views.Search,name='search'),
    path('mycart/',views.MyCart,name='mycart'),
    path('removecart/<product_id>',views.RemoveCart,name='removecart'),
    path('categoy_products/addcart/',views.addCart,name='addcart'),
    path('search/addcart/',views.addCart,name='addcart'),
    path('addcart/',views.addCart,name='addcart'),
    path('categoy_products/<category>',views.categoy_products,name='categoy_products'),

    #seller routes
    path('addproduct',views.AddProductForm),
    path('newproduct/',views.CreatProduct, name="newproduct"),
    path('dashboard/',views.sellerDashboard),

    path('verify_otp/',views.opt_page),

    path('verify_otp/confirm_otp/',views.confirm_otp, name="confirm_otp"),
    path('/dashboard/deleteproduct/<product_id>',views.deleteproduct, name="deleteproduct"),

    path('read_services/',views.read_services,name="read_services"),
    path('book_now/',views.Book_now,name="book_now.html"),

]