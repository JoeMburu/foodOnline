from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from marketplace.context_processors import get_cart_counter
from menu.models import Category, FoodItem
from vendor.models import Vendor
from marketplace.models import Cart

# Create your views here.
def marketplace(request):
    vendors  = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }   
    return render(request, 'marketplace/listings.html', context)


def vendorDetail(request, vendor_slug, category_slug=None):  
    selected_category = None    

    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor)
    food_items = FoodItem.objects.filter(vendor=vendor)
    
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        food_items = FoodItem.objects.filter(vendor=vendor, category=selected_category)

    # Build cart_quantities for the browsing user
    cart_quantities = {}
    if request.user.is_authenticated:
        # Only cart rows for this user AND only for the food items shown on this page
        cart_rows = (
            Cart.objects
            .filter(user=request.user, fooditem__in=food_items)
            .values_list('fooditem_id', 'quantity')
        )
        cart_quantities = dict(cart_rows)        

    context = {
        'vendor': vendor,
        'categories': categories,
        'food_items': food_items, 
        'selected_category': selected_category,
        'cart_quantities': cart_quantities
    }
    return render(request, 'marketplace/vendorDetail.html', context)   

def addToCart(request, food_id):
    print("Add to cart called")
    if request.user.is_authenticated:
        if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                   # Check if the food item already exists in the cart
                   cart_item = Cart.objects.get(user=request.user, fooditem=fooditem)
                   cart_item.quantity += 1
                   cart_item.save()
                   cart_count = get_cart_counter(request)['cart_count']                  
                   
                   return JsonResponse({'status':'success', 'message':'Food item already in cart.', 'cart_quantity': cart_item.quantity, 'cart_count': cart_count})
                except:
                    cart_item = Cart.objects.create(
                        user = request.user,
                        fooditem = fooditem,
                        quantity = 1
                    )
                    cart_count = get_cart_counter(request)['cart_count']
                    return JsonResponse({'status':'success', 'message':'Food item added to cart.', 'cart_quantity': cart_item.quantity, 'cart_count': cart_count})
            except:
                return JsonResponse({'status':'failed', 'message':'This fooditem does not exist.'})
        else:
            return JsonResponse({'status':'failed', 'message':'Invalid request!'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please login to continue.'})
def subtractFromCart(request, food_id):   
    if request.user.is_authenticated:
        if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                   # Check if the food item already exists in the cart
                   cart_item = Cart.objects.get(user=request.user, fooditem=fooditem)
                   if cart_item.quantity > 1:
                       cart_item.quantity -= 1
                       cart_item.save()
                       cart_count = get_cart_counter(request)['cart_count']  
                       print("Cart count after subtraction:", cart_count)                
                       return JsonResponse({'status':'success', 'message':'Subtracted item from cart.', 'cart_quantity': cart_item.quantity, 'cart_count': cart_count})
                   else:
                       cart_item.delete()
                       cart_count = get_cart_counter(request)['cart_count']
                       return JsonResponse({'status':'success', 'message':'Item removed from cart.', 'cart_quantity': 0, 'cart_count': cart_count})
                except:
                    return JsonResponse({'status':'failed', 'message':'Food item not in cart.'})
            except:
                return JsonResponse({'status':'failed', 'message':'This fooditem does not exist.'})
        else:
            return JsonResponse({'status':'failed', 'message':'Invalid request!'})
    else:       
        return JsonResponse({'status':'login_required', 'message':'Please login to continue.'})