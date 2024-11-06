from django.shortcuts import render, redirect
from ecommapp.models import *
from django.db.models import Sum 
from userauth.models import *
from useradmin.forms import *
from django.contrib import messages
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from useradmin.decoraters import admin_required

import datetime 
# Create your views here.

@admin_required
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

@admin_required
def product_list(request):
    all_products = Product.objects.all().order_by('-id')
    all_category = Category.objects.all()
    context = {
        'all_products':all_products,
        'all_category':all_category
    }
    return render(request,'useradmin/product.html',context)

@admin_required
def add_product(request):
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.vendor = Vendor.objects.get(id=1)
            new_form.product_status = 'published'
            new_form.save()
            form.save_m2m()
            
            print(new_form)
            return redirect('useradmin:dashboard')
    else:
        form = AddProduct()
    
    return render(request,'useradmin/add-product.html',{'form':form})

@admin_required
def update_product(request,pid):
    
    product = Product.objects.get(id=pid)
    
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES,instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.vendor = Vendor.objects.get(id=1)
            new_form.product_status = 'published'
            new_form.save()
            form.save_m2m()
            
            print(new_form)
            return redirect('useradmin:products')
    else:
        form = AddProduct(instance=product)
    
    return render(request,'useradmin/edit-product.html',{'form':form,'product':product})

@admin_required
def delete_product(request,pid):
    product = Product.objects.get(id=pid)
    product.delete()
    return redirect('useradmin:products')

@admin_required
def orders(request):
    orders = Cartorder.objects.all()
    context = {
        'orders':orders
    }
    return render(request,'useradmin/orders.html',context)

@admin_required
def order_details(request,id):
    order = Cartorder.objects.get(oid=id)
    products = CartorderItem.objects.filter(order = order)
    context = {
        'products':products,
        'order':order
    }
    return render(request,'useradmin/order-details.html',context)

@admin_required
@csrf_exempt
def change_order_status(request,oid):
    order = Cartorder.objects.get(oid=oid)
    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
        if status in dict(STATUS_CHOICES).keys():
            order.product_status = status
            order.save()
        messages.success(request,'Order status updated successfully')
    else:
        messages.error(request,'Something went wrong')
    return redirect('useradmin:orderdetails',order.oid)

@admin_required
def shop_page(request):
    product = Product.objects.all()
    revenue = Cartorder.objects.aggregate(price=Sum('price'))
    total_sales = CartorderItem.objects.filter(order__paid_status=True).aggregate(price=Sum('qty'))
    context = {
        'product':product,
        'revenue':revenue,
        'total_sales':total_sales
    }
    
    return render(request,'useradmin/shop.html',context)

@admin_required
def reviews(request):
    reviews = product_review.objects.all()
    context = {
        'reviews':reviews
    }
    
    return render(request,'useradmin/reviews.html',context)

@admin_required
def settings(request):
    profile = profile_details.objects.get(user=request.user)
    if request.method == 'POST':
        image = request.FILES.get('image')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        country = request.POST.get('country')
        
        if image != None:
            profile.image = image
            
        profile.full_name = full_name
        profile.phone = phone
        profile.address = address
        profile.country = country
        
        profile.save()
        messages.success(request,'Profile updated successfully')
        return redirect('useradmin:settings')
    
    context = {
        "profile":profile
    }
    return render(request,'useradmin/settings.html',context)

@admin_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if old_password == new_password:
            messages.error(request,'New password cannot be same as old password')
            return redirect('useradmin:changepassword')
        
        if confirm_password != new_password:
            messages.error(request,'Password does not match')
            return redirect('useradmin:changepassword')
        
        if check_password(old_password,user.password):
            user.set_password(new_password) 
            user.save()
            messages.success(request,'Password changed successfully')
            return redirect('useradmin:changepassword')
        else:
            messages.error(request,'Old password is incorrect')
            return redirect('useradmin:changepassword')
    return render(request,'useradmin/changepassword.html')