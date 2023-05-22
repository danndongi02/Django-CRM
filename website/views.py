from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Home view
def home(request):
    # Grab all the records from the table
    records = Record.objects.all()

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
                request, "Incorrect Username Or Password. Please Try Again...")
            return redirect('home')

    else:
        return render(request, 'home.html', {'records': records})

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

# View Customer Records


def customer_record(request, pk):
    # Check if logged in
    if request.user.is_authenticated:
        # Look up records
        customer_record = Record.objects.get(id=pk)

        return render(request, 'record.html', {'customer_record': customer_record})

    else:
        messages.success(request, "You Must Be Logged In To View That Page!")

        return redirect('home')

# Deleting a record


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete = Record.objects.get(id=pk)
        delete.delete()

        messages.success(request, "Record Deleted Successfully!")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Delete A Record!")
        return redirect('home')

# Add Record


def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Customer Successfully Added")
                return redirect('home')

        return render(request, 'add_record.html', {"form": form})

    else:
        messages.success(request, "You Are Not Logged In!")
        return redirect('home')

# Update Record


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated Successfully!")
            return render(request, 'record.html', {'customer_record': current_record})

        return render(request, 'update_record.html', {"form": form, "customer_record": current_record})

    else:
        messages.success(request, "You Are Not Logged In!")
        return redirect('home')
