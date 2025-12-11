from vendor.models import Vendor

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user.id)
    except Vendor.DoesNotExist:
        vendor = None
    return dict(vendor=vendor)

    
    