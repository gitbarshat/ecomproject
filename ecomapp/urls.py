from django.urls import path
from .views import *

app_name = 'ecomapp'
urlpatterns = [
    path('',HomeView.as_view(),name ='home'),
    path('about/',AboutView.as_view(),name ='about'),
    path('contact/',ContactView.as_view(),name ='contact'),
    path('allproducts/',AllproductsView.as_view(),name ='allproducts'),

    path('productdetail/<slug:slug>/',ProductdetailView.as_view(),name = 'productdetail'),
    path('add-to-cart/<int:pro_id>/',AddtocartView.as_view(),name = 'addtocart'),
    path('mycart/',MycartView.as_view(),name = 'mycart'),
    path('managecart/<int:cp_id>/',ManagecartView.as_view(),name = 'managecart'),
    path('emptycart/',EmptycartView.as_view(),name = 'emptycart'),

    path('checkout/',CheckoutView.as_view(), name = 'checkout'),
    path('register/',CustomerregistrationView.as_view(),name = 'customerregistration'),
    path('logout/',CustomerlogoutView.as_view(),name = 'customerlogout'),
    path('login/',CustomerloginView.as_view(),name = 'customerlogin'),


]