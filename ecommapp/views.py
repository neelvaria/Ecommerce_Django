from django.shortcuts import render , get_object_or_404
from ecommapp.forms import *
from ecommapp.models import *
from django.db.models import Count,Avg
from taggit.models import Tag
from django.http import JsonResponse
from django.template.loader import render_to_string


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
    make_review = True
    if request.user.is_authenticated:
        user_review_count = product_review.objects.filter(user=request.user, product=products).count()
        if user_review_count > 0:
            make_review = False
    else:
        make_review = True
    
    context = {
        "products":products,
        "p":p_images,
        "pro":product,
        "related_products": related_products,
        "reviews":reviews,
        "avg_rating":avg_rating,
        "review_form":review_form,
        "make_review":make_review

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
    
def search_view(request):
    query = request.GET.get('q')
    
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    context = {
        "products":products,
        "query":query
    }
    return render(request,'search.html',context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    
    min_price = request.GET.get("min_price", 0)  # Default to 0 if missing
    max_price = request.GET.get("max_price", float('inf'))
    
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    products = products.filter(price__gte=min_price).filter(price__lte=max_price)
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors)
        
    context = render_to_string("async/product_list.html",{"products":products})
    return JsonResponse({"context":context})

def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET.get("id"))] = {
        'title':request.GET.get("title"),
        'price':request.GET.get("price"),
        'qty':request.GET.get("qty"),
        'image':request.GET.get("image"),
        'pid':request.GET.get("pid"),
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET.get("id")) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET.get("id"))]['qty'] = int(cart_data[str(request.GET.get("id"))]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj'])})
    