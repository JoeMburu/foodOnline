from django.shortcuts import render, redirect

from accounts.utils import detectUser
from vendor.forms import VendorRegistrationForm
from .forms import UserRegistrationForm
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied



# authorization methods
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied  

# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered and logged in.')
        return redirect('dashboard')  # Redirect to a dashboard or home page if already logged in   
    elif request.method == 'POST':
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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered and logged in.')
        return redirect('dashboard')  # Redirect to a dashboard or home page if already logged in
    elif request.method == 'POST':
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

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')  # Redirect to a dashboard or home page if already logged in
    elif request.method == 'POST':
        # Authenticate user
        email = request.POST.get('email') # request.Post['email']
        password = request.POST.get('password')
        # Add your authentication logic here. Django has authentication built-in.
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')  # Redirect to a dashboard or home page 
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')  # Redirect back to login page
    else:
        return render(request, 'accounts/login.html')
    
def logout(request):
    auth.logout(request)
    messages.info(request, 'You have been logged out.')        
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    getUserUrl = detectUser(user)
    return redirect(getUserUrl)
     
