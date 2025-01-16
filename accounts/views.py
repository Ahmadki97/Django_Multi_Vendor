from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from vendor.models import Vendor
from django.contrib import messages
import logging

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully.")
            return redirect('registerUser')
        else:
            logging.error(f"Error in User registration form: {form.errors}")
            messages.error(request, f"There was an error with your registration {form.errors}")
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        "form": form,
        }
    return render(request, 'accounts/registerUser.html', context)



def registerVendor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid() :
            user = form.save(commit=False)
            user.role = User.RESTURANT
            user.set_password(user.password)
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, f"Your Account has been registered successfully, please wait for the approval.")
            logging.info(f"registerVendor() function, New User & Vendor is added to the db Successfully")
            return redirect('registerVendor')
        else:
            logging.error(f"Error in Vendor Registeration Process {form.errors or vendor_form.errors}")
            messages.error(request, f"There was an error with your registration {form.errors or vendor_form.errors}")
            return redirect('registerVendor')  # Redirect back to the form if there are errors
    else:    
        form = UserForm()
        vendor_form = VendorForm()

        context = {
            'form': form,
            'v_form': vendor_form,
        }
        return render(request, 'accounts/registerVendor.html', context=context)