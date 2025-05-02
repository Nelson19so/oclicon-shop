from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginFrom
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.

# registration view set
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('home')

    else:
        form = UserRegistrationForm()

    context = {"form":form}
    return render(request, 'accounts/authentication/register.html', context)


# logout view set 
def logout_view(request):
    logout(request)
    messages.info(request, 'logged out successfully')
    return redirect("home")