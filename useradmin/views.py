from django.shortcuts import render, redirect
from ecommapp.models import *
from django.db.models import Sum 
from userauth.models import *

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
    