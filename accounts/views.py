from django.shortcuts import render, redirect
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
            return render(request, 'accounts/register_user.html', {'form': form})

    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register_user.html', context)

def registerRestaurant(request):
    pass