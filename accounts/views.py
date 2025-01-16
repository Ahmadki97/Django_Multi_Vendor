from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
import logging

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        print(f"data in the request is {request.POST}")
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully.")
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        "form": form,
        }
    return render(request, 'accounts/registerUser.html', context)