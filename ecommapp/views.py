from django.shortcuts import render , get_object_or_404
from ecommapp.forms import *
from ecommapp.models import *
from django.db.models import Count,Avg
from taggit.models import Tag
from django.http import JsonResponse

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
    product = Product.objects.filter(category=products.category).exclude(p_id=p_id)
    related_products = Product.objects.filter(category=products.category).exclude(p_id=p_id)[:4]
    # products = get_object_or_404(Product,p_id=p_id)
    
    p_images = products.p_image.all()
    
    #getting all reviews
    reviews = product_review.objects.filter(product=products).order_by("-id")
    
    #getting average reviews
    avg_rating = product_review.objects.filter(product=products).order_by("-id").aggregate(Avg("rating"))

    #Product review form
    review_form = productreviewform()
    
    context = {
        "products":products,
        "p":p_images,
        "pro":product,
        "related_products": related_products,
        "reviews":reviews,
        "avg_rating":avg_rating,
        "review_form":review_form

    }
    return render(request,'product_details.html',context)

def tags_list(request,tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        products = products.filter(tags__in=[tag])
        
        # print(products)
        # print(tag)
    
    context = {
        "products":products,
        "tag":tag
    }
    return render(request,'tag_list.html',context)

def ajax_add_review(request,p_id):
    product = Product.objects.get(pk=p_id)
    user = request.user
    
    review = product_review.objects.create(
        user = user,
        product = product,
        review = request.POST.get("review"),
        rating = request.POST.get("rating")
    )
    
    context = {
        'user' : user.username,
        'review' : request.POST['review'],
        'rating' : request.POST['rating'],
    }
    
    average_reviews = product_review.objects.filter(product=product).aggregate(Avg("rating"))
    return JsonResponse(
        {
            'bool':True,
            'context':context,
            'avg_reviews':average_reviews
        }
    )
    