from django.shortcuts import render, redirect, HttpResponse
from .models import Register
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'loginReg_app/index.html')

def register(request):
    # Extract information from registration form
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    pwd = request.POST['password']
    pwd_confirm = request.POST['pwd_confirm']

    # Verify if user tries to register again with same credentials
    registerChk = Register.registerManager.chkRegister(email)
    if (registerChk):
        messages.error (request, "User already exists!")
    else:
        # Verifying registration process
        fnChk, msg = Register.registerManager.validateFN(first_name)  # Validate first name
        if (not fnChk):
            messages.error(request, msg)
        lnChk, msg = Register.registerManager.validateLN(last_name)  # Validate last name
        if (not lnChk):
            messages.error(request, msg)
        emailChk, msg = Register.registerManager.validateEmail(email)  # Validate email
        if (not emailChk):
            messages.error(request, msg)
        pwdChk, msg = Register.registerManager.validatePwd(pwd)  # Validate password
        if (not pwdChk):
            messages.error(request, msg)
        
        # Verify password confirmation matches password
        if (pwd == pwd_confirm):
            pwdConfirmChk = True
        else:
            messages.error(request, "Passwords don't match!")
            pwdConfirmChk = False

        if (fnChk and lnChk and emailChk and pwdChk and pwdConfirmChk):  # All fields are valid
            messages.success(request, "Success! Welcome, %s! Successfully registered in!" % first_name)
            Register.objects.create(first_name=first_name, last_name=last_name, email=email, password=pwd, pwd_confirm=pwd_confirm)
            return redirect('/success')

    # All fields are not valid
    return redirect('/')

def login(request):
    # Extracting information from login form
    login_email = request.POST['login_email']
    login_password = request.POST['login_password']

    # Check if user is already registered
    registerChk = Register.registerManager.chkRegister(login_email)
    if (registerChk):
        messages.success(request, "Successfully logged in!")
        return redirect('/success')
    
    messages.error(request, "Please register!")
    return redirect('/')

def success(request):
    return render(request, 'loginReg_app/success.html')