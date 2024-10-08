from django.shortcuts import render
from ecommapp.models import *
from django.db.models import Count
from django.shortcuts import get_object_or_404 

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

def vendor_list(request):    
    vendors = Vendor.objects.all()
    context = {
        "vendors":vendors
    }
    return render(request,'vendor_list.html',context)

def vendor_details_view(request,v_id):
    vendor = Vendor.objects.get(v_id=v_id)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    context = {
        "vendor":vendor,
        "products":products
    }
    return render(request,'vendor_details.html',context)

def product_details_view(request,p_id):
    products = Product.objects.get(p_id=p_id)
    
    # products = get_object_or_404(Product,p_id=p_id)
    
    p_images = products.p_image.all()
    
    context = {
        "products":products,
        "p":p_images
    }
    return render(request,'product_details.html',context)