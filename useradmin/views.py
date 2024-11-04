from django.shortcuts import render, redirect
from ecommapp.models import *
from django.db.models import Sum 
from userauth.models import *
from useradmin.forms import *

import datetime 
# Create your views here.

def vendor_dashboard(request):
    revenue = Cartorder.objects.aggregate(price=Sum('price'))
    total_order = Cartorder.objects.all()
    all_products = Product.objects.all()
    all_catgeory = Category.objects.all()
    new_customer = User.objects.all().order_by('-id')
    latest_order = Cartorder.objects.all()
    
    this_month = datetime.datetime.now().month
    monthly_revenue = Cartorder.objects.filter(order_date__month = this_month).aggregate(price=Sum('price'))
    context = {
        'revenue':revenue,
        'total_order':total_order,
        'all_products':all_products,
        'all_catgeory':all_catgeory,
        'new_customer':new_customer,
        'latest_order':latest_order,
        'monthly_revenue':monthly_revenue
    }
    
    return render(request,'useradmin/dashboard.html',context)

def product_list(request):
    all_products = Product.objects.all()
    all_category = Category.objects.all()
    context = {
        'all_products':all_products,
        'all_category':all_category
    }
    return render(request,'useradmin/product.html',context)

def add_product(request):
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.vendor = request.user
            new_form.product_status = 'published'
            new_form.save()
            form.save_m2m()
            
            print(new_form)
            return redirect('useradmin:dashboard')
    else:
        form = AddProduct()
    
    return render(request,'useradmin/add-product.html',{'form':form})