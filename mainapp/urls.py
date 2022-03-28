from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.Index.as_view(),name='home'),
    path('shop',views.Shop.as_view(),name='shop'),
    path('shops/<int:id>/',views.Shop_Single,name='shops'),
    path('contact',views.Contact.as_view(),name='contact'),
    path('add_cart/<int:id>',views.add_cart,name='add_cart'),
    path('search',views.search,name='search'),
    path('delete_cart/<int:id>',views.remove_cart,name='remove'),
    path('cart',views.CartList.as_view(),name='cart'),
    path('about',views.About.as_view(),name='about'),
    path('contact',views.contact,name='contact'),






]