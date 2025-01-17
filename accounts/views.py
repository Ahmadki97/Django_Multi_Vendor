from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from vendor.models import Vendor
from django.contrib import messages, auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
import logging

# Create your views here.


# Restrict the Customer from accessing the Vendor Dashboard
def checkRoleVendor(user: User):
    if user.role == User.RESTURANT:
        return True
    else:
        raise PermissionDenied


# Restrict the Vendor from accessing the Customer Dashboard
def checkRoleCustomer(user: User):
    if user.role == User.CUSTOMER:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
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
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
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
    


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"You are now logged in, {user.username}")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid credentials, please try again.")
            return redirect('login')
    return render(request, 'accounts/login.html') 



def logout(request):
    auth.logout(request)
    messages.info(request, f"You are logged out.")
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirect_url = detectUser(user)
    return redirect(redirect_url)


@login_required(login_url='login')
@user_passes_test(checkRoleCustomer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(checkRoleVendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')



