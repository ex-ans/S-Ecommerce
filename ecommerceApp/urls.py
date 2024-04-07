from django.contrib import admin
from django.urls import path
from ecommerceApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('' , views.index , name='index'), 
    path('signup' , views.signup , name='signup'), 
    path('signin' , views.signin , name='signin'), 
    path('verification' , views.verification , name='verification'), 
    path('logout_user' , views.logout_user, name="logout_user"),
    path('productpage/<int:product_id>' , views.productpage , name='productpage'),
    path('deleteCart/<int:id>' , views.deleteCart , name='deleteCart'),
    path('cart' , views.viewCart , name='viewCart'),
    path('checkout/<int:id>' , views.checkout , name='checkout'),
    path('u_orders' , views.u_orders , name='u_orders'),
    path('search' , views.search , name='search'),
    # path('deleteorder/<int:id>' , views.deleteorder , name='deleteorder'),
] +static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
