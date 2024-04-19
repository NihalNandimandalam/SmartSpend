from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('display')
        else:
            return view_function(request, *args,**kwargs)
    return wrapper_function

def allowed_users(allowed_roles=[]):
    def decorater(view_function):
        def wrapper_function(request, * args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponse("You don't have access to this page")
        return wrapper_function
    return decorater

def customer_only(view_function):
    def wrapper_function(request, * args, **kwargs):
        
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'admin':
            return render(request, 'transcations/user.html',{})
        if group == 'customer':
            return view_function(request, *args, **kwargs)
    return wrapper_function
