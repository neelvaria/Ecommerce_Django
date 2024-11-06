from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_superuser != True:
            messages.error(request,'You are not authorized to view this page')
            return redirect('userauth:login')
        return view_func(request, *args, **kwargs)
    return wrapper_function