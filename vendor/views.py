from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest
from django.contrib import messages
from .models import Vendor
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import checkRoleVendor
from .forms import VendorForm
# Create your views here.

@login_required(login_url='login')
@user_passes_test(checkRoleVendor)
def profile(request: HttpRequest):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('vprofile')
        else:
            messages.error(request, profile_form.errors or vendor_form.errors)
            return redirect('vprofile')
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
        context = {
            'profile_form': profile_form,
            'vendor_form': vendor_form,
            'profile': profile,
            'vendor': vendor
        }
        return render(request, 'vendor/vprofile.html', context=context)