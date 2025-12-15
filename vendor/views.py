from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import VendorRegistrationForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from accounts.views import check_role_vendor
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorRegistrationForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vendorProfile')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorRegistrationForm(instance=vendor)
    context = {
        'profile_form': profile_form,   
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendorProfile.html', context)