from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from menu.forms import CategoryForm
from .forms import VendorRegistrationForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from menu.models import Category, FoodItem
from accounts.views import check_role_vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

# Create your views here.
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


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


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menuBuilder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    
    context = {       
       'categories': categories,        
    }
    return render(request, 'vendor/menuBuilder.html', context)

def foodItemsByCategory(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category, pk=pk)
    foodItems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'foodItems': foodItems,
        'category': category,
    }               
    return render(request, 'vendor/foodItemsByCategory.html', context)

def addCategory(request):    
    vendor = get_vendor(request)         
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            try:
                category.save() 
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
                                        
                messages.error(request, 'Please correct the error below.') 
            else:
                messages.success(request, 'Category added successfully!')
                return redirect('menuBuilder')  
        else:
            messages.error(request, 'Please correct the error below.')    

    else:
        form = CategoryForm()
    context = {
        'form': form,
        'vendor': vendor,
    }                          
    return render(request, 'vendor/addCategory.html', context)

def editCategory(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk, vendor=vendor)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category) # Update existing instance
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            try:
                category.save() 
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
                                        
                messages.error(request, 'Please correct the error below.') 
            else:
                messages.success(request, 'Category updated successfully!')
                return redirect('menuBuilder')  
        else:
            messages.error(request, 'Please correct the error below.')    

    else:
        form = CategoryForm(instance=category)       
    context = {
        'form': form,
        'category': category,
    }  
    return render(request, 'vendor/editCategory.html', context)

def deleteCategory(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk, vendor=vendor)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('menuBuilder')