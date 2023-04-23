from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm


# Home view
def home(request):
    # Check to see if user is logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully!")
            return redirect('home')
        else:
            messages.success(
                request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')

    else:
        return render(request, 'home.html', {})

# Logout the user


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


# Register a new user
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            # Authentication and log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful! Welcome!")
            return redirect('home')

    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})
