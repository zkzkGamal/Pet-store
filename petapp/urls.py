from django.urls import path
from django.contrib import admin
from . import views
from django_filters.views import FilterView
from .models import Product

urlpatterns = [
    path('',views.home,name = 'home'),
    path('product-detail/<slug:slug>',views.productDetailList,name = 'product-detailList'),
    path('product-detail/',views.productDetail,name = 'product-detail'),
    path('login',views.login,name = 'login'),
    path('signup',views.signup,name = 'signup'),
    path('checkout',views.checkout,name = 'checkout'),
    path('card',views.card,name = 'card'),
    path('add-product',views.addProduct,name = 'add-product'),
    path('add-pet',views.addPET,name = 'add-pet'),
    path('products',views.product,name = 'products'),
    path('product/<str:types>',views.product_types,name = 'product-sp'),
    path('product/catigory/<str:catigory>',views.product_catigory,name = 'product-ct'),
    path('seller',views.seller,name = 'seller'),
    path('DashBoard',views.dashBoard,name = 'DashBoard'),
    path('logout',views.logoutUser,name = 'logout'),
    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('doctor-sign',views.Doctor_signUP,name='doctor-sign' ),
    path('delete-product/<slug:slug>',views.deleteProduct,name='delete-product' ),
    path('edit-product/<slug:slug>',views.editProduct,name='edit-product' ),
    path("list/", FilterView.as_view(model=Product), name="list"),
    path('vetDash',views.vetDash , name='vetDash'),
    path('doctorcards',views.doctorcards, name='doctorcards'),
    path('doctor_details/<slug:slug>',views.doctor_details, name='doctor_details'),
    path('book-session/<int:session_id>/<slug:slug>',views.book_session, name='book-session'),
    
]