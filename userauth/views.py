from django.shortcuts import render ,  redirect
from userauth.forms import *
from django.contrib.auth import login, authenticate , logout
from django.contrib import messages
from django.conf import settings
from userauth.models import User

# User = settings.AUTH_USER_MODEL
# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username} successfully!!")
            new_user = authenticate(username = form.cleaned_data['email'], 
                                    password = form.cleaned_data['password1']) 
            login(request, new_user)
            return render(request,'page-login.html')
    else:
        form = UserRegisterForm()

        
    context = {
        'form':form,
    }
    return render(request,'page-register.html',context)

def login_view(request):
    if request.user.is_authenticated:
        print(request.user)
        return render(request,'index.html')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            users = User.objects.get(email = email)
            users = authenticate(request, email = email, password = password)
            
            if users is not None:
                login(request, users)
                messages.success(request,f"Logged in successfully!!")
                return redirect('ecommapp:index')
        
            # else:
            #     messages.warning(request,f"User with {email} does not exist!! Create an Account")
            
        except:
            messages.warning(request,f"User with {email} does not exist!!")

    return render(request,'page-login.html')

def logout_view(request):
    logout(request)
    request.session.flush()  # Clear the session data
    messages.warning(request,"You have been logged out!!")

    return redirect('userauth:login')