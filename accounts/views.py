from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.utils import detectUser, send_verification_email, send_password_reset_email
from vendor.forms import VendorRegistrationForm
from vendor.models import Vendor
from .forms import UserRegistrationForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



# Authorization methods
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
# Method to check for role of customer    
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
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            # Send success message
            send_verification_email(request, user)            
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
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.VENDOR
            user.set_password(password)
            user.save()

            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = user.userprofile
            vendor.save()
            # Send success message
            send_verification_email(request, user)            
            messages.success(request, 'Your vendor account has been registered successfully! Please wait for approval.')
            return redirect('login')  # Redirect to the same page or another page
        else:
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
     

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:        
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('myAccount')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Add logic to handle password reset email sending
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            if user:
                mail_subject = 'Reset Your Password'
                email_template = 'accounts/emails/reset_password_email.html'
                send_password_reset_email(request, user, mail_subject, email_template)
                messages.success(request, 'Password reset link has been sent to your email address.')
                return redirect('login')
        else:
            messages.error(request, 'No account found with the provided email address.')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgot_password.html')

def resetPasswordValidate(request, uidb64, token):
    try:        
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'The reset password link is invalid or has expired!')
        return redirect('myAccount')    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)            
            user.set_password(password)
            user.save()
            print("USER:", user)
            request.session.flush()
            messages.success(request, 'Password reset successful. You can now log in with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('resetPassword')
    return render(request, 'accounts/reset_password.html')