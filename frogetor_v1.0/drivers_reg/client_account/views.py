from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm, UpdateForm, UpdatePasswordForm

# Create your views here.
def pageStart(request):
    """
    """
    if request.user.is_authenticated:
        return render(request, 'client_account/page_start.html')
    else:
        messages.success(request, "U must be loged in")
        return redirect('login_view')

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            # add a msg of u were successfully loged in
            return redirect('pageStart')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect('login_view')
    
    else:
        return render(request, "auth/auth-login.html", {})

#logout view
def logout_view(request):
    # using the django built in function
	logout(request)
	messages.success(request, ("You Were Logged Out!")) # this dosen't appear
	return redirect('login_view')


# registration view
def registration_view(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			print("form is valid")
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
            
			messages.success(request, ("Registration Successful! You can now Login"))
			return redirect('login_view')
	else:
		print("form is not valid")
		form = RegistrationForm()
        
	return render(request, 'auth/auth-register.html', {'form':form})

# this view is used o update the user profile
def edit_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User has been Updated!!!")
            return redirect('pageStart')
        return render(request, 'client_account/edit-profile.html', {'user_form':user_form})
    
    else:
        messages.success(request, "U must be loged in")
        return redirect('login_view')
      
def edit_password(request):
    # we ned to make sure that the user is authenticated aka logged in
    if request.user.is_authenticated:
        current_user = request.user
        # did they fill out the form ?
        if request.method == 'POST':
            # grap the form
            form = UpdatePasswordForm(current_user, request.POST)
            # check if the form is valid
            if form.is_valid():
                # then save
                form.save()
                # then print a successful messege in the nex web page --> log in!
                messages.success(request, "Your Password Has been Updated, you need to log in ")
                return redirect('login_view')
            else:
                # pass the django authentication errors
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(request, 'client_account/edit-password.html', {'form':form})
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'client_account/edit-password.html', {'form':form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('login_view')
      

def error_404(request, exception=None):
        data = {}
        return render(request,'auth/auth-404.html', data)

def error_500(request,  exception=None):
        data = {}
        return render(request,'auth/auth-500.html', data)
