from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from .models import LoginHistory
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password  # Import make_password
import hashlib
from django.contrib.auth.hashers import check_password

# Create your views here.
def pageStart(request):
    return render(request, 'client_account/page_start.html')


# def login_view(request):
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
            print(UserProfile.objects.all().values('username', 'email'))
            # Authenticate user: function provided by Django's authentication system
            user = authenticate(request, username=username, password=password)
            
            # # Retrieve the user by username from your custom user table
            # try:
            #     user = UserProfile.objects.get(username=username)
            # except UserProfile.DoesNotExist:
            #     user = None
            # login(request, user)
            print(user)
            if user is not None:
                print("user is not none")
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

# def hash_password(password):
    """
    Hashes a password using SHA-256 algorithm.
    """
    password_bytes = password.encode('utf-8')
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return hashed_password

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # Retrieve user from the database
        try:
            user_profile = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            user_profile = None

        print(user_profile.username, user_profile.password)
        # Check if the user exists and the password is correct
        if user_profile is not None:
            if check_password(password, user_profile.password):
                # Authenticate the user
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    # Login the user
                    login(request, user)
                    # Redirect to a success page
                    return redirect('pageStart')
                else:
                    # Handle the case where authentication fails
                    return render(request, 'auth/auth-login.html', {'error_message': 'Authentication failed.'})
            else:
                return render(request, 'auth/auth-login.html', {'error_message': 'Authentication failed.'})
        else:
            # Handle the case where the username or password is incorrect
            return render(request, 'auth/auth-login.html', {'error_message': 'Invalid username or password.'})
    else:
        # Render the login form
        return render(request, 'auth/auth-login.html')

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
