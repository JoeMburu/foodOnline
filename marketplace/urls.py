from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.marketplace, name='marketplace'),  
    path('<slug:vendor_slug>/', views.vendorDetail, name='vendorDetail'),
    path('<slug:vendor_slug>/category/<slug:category_slug>/', views.vendorDetail, name='vendorCategory'),
    path('addToCart/<int:food_id>/', views.addToCart, name='addToCart'),
    path('subtractFromCart/<int:food_id>/', views.subtractFromCart, name='subtractFromCart'),
    
]