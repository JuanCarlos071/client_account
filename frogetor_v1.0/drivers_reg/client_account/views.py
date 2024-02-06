from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from .models import LoginHistory
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password  # Import make_password

# Create your views here.
def pageStart(request):
    return render(request, 'client_account/page_start.html')


def login_view(request):
    # the the request is POST
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Form submission
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            print("Username:", username)
            print("Password:", password)
            print("Remember Me:", remember_me)
            # Authenticate user: function provided by Django's authentication system
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                # Login successful ->  function to log the user in.
                # function used here is not a built-in Django function
                # but rather a placeholder for a typical login mechanism in Django
                login(request, user)
                # Create login history record
                LoginHistory.objects.create(user=user, remember_me=remember_me)
                # Redirect user to a success page
                return redirect('pageStart')
            else:
                # Invalid login, handle accordingly
                # retun error msg
                form.add_error('username', 'Invalid username.')
                form.add_error('username', 'Invalid password.')
        else:
             print("form was not valid")
             for field, errors in form.errors.items():
                print(f"Field '{field}': {', '.join(errors)}")
    # else Just give the form variable to the page that will be rendred
    else:
        form = LoginForm()
    # the page to render anyways
    return render(request, 'auth/auth-login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        print("there is a post request")
        # get the data from the form
        form = RegistrationForm(request.POST)
        for field in form:
                print(field.label)
        if form.is_valid():
            
            # Check if passwords match
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                form.add_error('confirm_password', "Passwords do not match")
                return render(request, 'auth/auth-register.html', {'form': form})

            # Hash the password before saving
            form.cleaned_data['password'] = make_password(password)
            print("form is valid")
            form.save()
            return redirect('login_view')
    else:
        form = RegistrationForm()
    return render(request, 'auth/auth-register.html', {'form': form})


def error_404(request, exception=None):
        data = {}
        return render(request,'auth/auth-404.html', data)

def error_500(request,  exception=None):
        data = {}
        return render(request,'auth/auth-500.html', data)
