from .models import Cart


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:        
      try:
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
           for item in cart_items:
              cart_count += item.quantity
        else:
           cart_count = 0
      except:
        cart_count = 0
    
    return dict(cart_count=cart_count)

    
def get_cart_amount(request):
    total_amount = 0
    subtotal = 0
    tax = 0
    if request.user.is_authenticated:        
      try:
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
           for item in cart_items:
              subtotal += item.fooditem.price * item.quantity
        else:
           subtotal = 0
      except:
        subtotal = 0

      tax = (2 * subtotal)/100
      total_amount = subtotal + tax
    
    return dict(total_amount=total_amount, subtotal=subtotal, tax=tax)