from django.shortcuts import render
from ecommapp.models import *
from django.db.models import Count 

# Create your views here.

def index(request):
    products = Product.objects.all().order_by('-id')
    # products = Product.objects.filter(featured=True)
    context = {
        'products':products
    }
    return render(request,'index.html',context)

def product_list(request):
    # products = Product.objects.all().order_by('-id')
    products = Product.objects.filter(product_status="published")
    context = {
        'products':products
    }
    return render(request,'product_list.html',context)

def category_list(request):
    # categories = Category.objects.all().annotate(product_count=Count('category'))
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request,'category_list.html',context)

def category_product_list(request,cid):
    category = Category.objects.get(c_id=cid)
    products = Product.objects.filter(product_status="published",category=category)
    
    context = {
        "category":category,
        "products":products,
    }
    return render(request,'category_product_list.html',context)