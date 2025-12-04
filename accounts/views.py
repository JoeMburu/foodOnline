from django.shortcuts import render, redirect

from vendor.forms import VendorRegistrationForm
from .forms import UserRegistrationForm
from .models import User
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully!')
            # You can add a redirect or success message here
            return redirect('registerUser')  # Redirect to the same page or another page
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'accounts/register_user.html', {'form': form})

    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register_user.html', context)

def registerVendor(request):
    if request.method == 'POST':
        # store data and create user
        form = UserRegistrationForm(request.POST)
        vendor_form = VendorRegistrationForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            user = form.save(commit=False)
            user.role = User.VENDOR
            user.save()

            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = user.userprofile
            vendor.save()

            messages.success(request, 'Your vendor account has been registered successfully! Please wait for approval.')
            return redirect('registerVendor')  # Redirect to the same page or another page
        else:
            print("INVALID FORM")
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'accounts/register_vendor.html', {'form': form, 'vendor_form': vendor_form})
    else:
        form = UserRegistrationForm()
        vendor_form = VendorRegistrationForm()
        context = {
            'form': form,
            'vendor_form': vendor_form
        }
        return render(request, 'accounts/register_vendor.html', context)

        
    