from django.shortcuts import render
from .models import Vendor
# Create your views here.


def profile(request):
    return render(request, 'vendor/vprofile.html')