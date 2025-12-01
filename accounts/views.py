from django.shortcuts import render

# Create your views here.
def registerUser(request):
    return render(request, 'accounts/register_user.html')

def registerRestaurant(request):
    return render(request, 'accounts/register_restaurant.html')