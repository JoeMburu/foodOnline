from django.urls import path, include
from . import views
from accounts import views as Accounts_Views

urlpatterns = [
  path('', Accounts_Views.vendorDashboard, name='vendor'), 
  path('profile/', views.vendorProfile, name='vendorProfile'), 
  #path('registerUser/', views.registerUser, name='registerUser'), 
   

]