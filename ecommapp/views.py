from django.shortcuts import render , get_object_or_404 , redirect
from ecommapp.forms import *
from ecommapp.models import *
from django.db.models import Count,Avg
from taggit.models import Tag
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings

#paypal stuff
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
import calendar
from datetime import datetime
from django.db.models.functions import *
from userauth.models import *

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
@login_required
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
            cart_data[str(request.GET.get("id"))]['qty'] = int(cart_product[str(request.GET.get("id"))]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj'])})

def cart_view(request):
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, p_data in request.session['cart_data_obj'].items():
            cart_total_amount += float(p_data['price']) * int(p_data['qty']) 
        return render(request,'cart.html',{"cart_data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request,"Your cart is empty!!!")
        return redirect('ecommapp:index')

def delete_from_cart(request):
    product_id = str(request.GET.get("id"))
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, p_data in request.session['cart_data_obj'].items():
            cart_total_amount += float(p_data['price']) * int(p_data['qty'])
             
    context = render_to_string("async/cart-list.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems':len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET.get("id"))
    qty = str(request.GET.get("qty"))
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(product_id)]['qty'] = qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, p_data in request.session['cart_data_obj'].items():
            cart_total_amount += float(p_data['price']) * int(p_data['qty'])
             
    context = render_to_string("async/cart-list.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems':len(request.session['cart_data_obj'])})

def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0
    
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['mobile'] = mobile
        request.session['address'] = address
        request.session['city'] = city
        request.session['state'] = state
        request.session['country'] = country
        
        if 'cart_data_obj' in request.session:
            for p_id, p_data in request.session['cart_data_obj'].items():
                total_amount += float(p_data['price']) * int(p_data['qty'])
    
            order = Cartorder.objects.create(
                user = request.user,
                price = total_amount,
                full_name = full_name,
                email = email,
                phone = mobile,
                address = address,
                city = city,
                state = state,
                country = country
            )
            
            del request.session['full_name']
            del request.session['email']
            del request.session['mobile']
            del request.session['address']
            del request.session['city']
            del request.session['state']
            del request.session['country']
    
            for p_id, p_data in request.session['cart_data_obj'].items():
                cart_total_amount += float(p_data['price']) * int(p_data['qty'])

                cart_order_product = CartorderItem.objects.create(
                    order = order,
                    invoice_no = 'INV-'+str(order.id),
                    item = p_data['title'],
                    image = p_data['image'],
                    qty = p_data['qty'],
                    price = p_data['price'],
                    total = float(p_data['price']) * int(p_data['qty']),  
                )
        return redirect('ecommapp:checkout', order.oid)
    return redirect('ecommapp:checkout', order.oid)

            
@login_required
def checkout_view(request,oid):
    order = Cartorder.objects.get(user=request.user, oid=oid)
    order_items = CartorderItem.objects.filter(order = order)
    
    if request.method == "POST":
        code = request.POST.get('code')
        coupon = Coupon.objects.filter(code = code,active=True).first()
        if coupon:
            if coupon in order.coupon.all():
                messages.warning(request,'Coupon already activated!!')
                return redirect('ecommapp:checkout', order.oid)
            else:
                messages.warning(request,'Coupon already applied!!')
                return redirect('ecommapp:checkout', order.oid)
        print(code)
    
    context = {
        'order':order,
        'order_items':order_items
    }
    
    return render(request,'checkout.html',context)
    
    #old checkout
    # cart_total_amount = 0
    # total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for p_id, p_data in request.session['cart_data_obj'].items():
    #         total_amount += float(p_data['price']) * int(p_data['qty'])
    
    #     order = Cartorder.objects.create(
    #         user = request.user,
    #         price = total_amount,
    #     )
    
    #     for p_id, p_data in request.session['cart_data_obj'].items():
    #         cart_total_amount += float(p_data['price']) * int(p_data['qty'])

    #         cart_order_product = CartorderItem.objects.create(
    #             order = order,
    #             invoice_no = 'INV-'+str(order.id),
    #             item = p_data['title'],
    #             image = p_data['image'],
    #             qty = p_data['qty'],
    #             price = p_data['price'],
    #             total = float(p_data['price']) * int(p_data['qty']),  
    #         )

    #     host = request.get_host()

    #     paypal_dict = {
    #         'business':settings.PAYPAL_RECEIVER_EMAIL,
    #         'amount':cart_total_amount,
    #         'item_name':"Order-Item-No-"+ str(order.id),
    #         'invoice':'INVOICE-' + str(order.id),
    #         'currency_code':'USD',
    #         'notify_url': f"http://127.0.0.1:8000{reverse('ecommapp:paypal-ipn')}",
    #         'return_url': f"http://127.0.0.1:8000{reverse('ecommapp:payment-success')}",
    #         'cancel_url': f"http://127.0.0.1:8000{reverse('ecommapp:payment-failed')}",
    #     }
    
    #     paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    #     print(paypal_form)
    
    #     try:
    #         active_address = Address.objects.get(user = request.user, status = True)
    #     except:
    #         messages.warning(request,"There are mutiple addresses. Please add a one address as default")
    #         active_address = None
    
    #     return render(request,'checkout.html',{"cart_data":request.session['cart_data_obj'], 
    #                 'totalcartitems':len(request.session['cart_data_obj']),
    #                 'cart_total_amount':cart_total_amount , 'paypal_form':paypal_form,
    #                 'active_address':active_address})

@login_required
def payment_completed_view(request):
    address = Address.objects.filter(user=request.user, status = True).first()
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, p_data in request.session['cart_data_obj'].items():
            cart_total_amount += float(p_data['price']) * int(p_data['qty'])
        
    return render(request,'payment-completed.html',{"cart_data":request.session['cart_data_obj'], 
                    'totalcartitems':len(request.session['cart_data_obj']),
                    'cart_total_amount':cart_total_amount,'address':address})

def payment_failed_view(request):
    return render(request,'payment-failed.html')

@login_required
def customer_dashboard(request):
    
    orders_list = Cartorder.objects.filter(user = request.user).order_by("-id")
    address = Address.objects.filter(user = request.user)
        
    orders = Cartorder.objects.annotate(month = ExtractMonth("order_date")).values("month").annotate(count = Count("id")).values('month', 'count')
    month = []
    total_orders = []
    
    for o in orders:
        month.append(calendar.month_name[o['month']])
        total_orders.append(o['count'])
    
    print(orders)
    print(month)
    print(total_orders)
    
    
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        new_address = Address.objects.create(user = request.user, address = address, contact = phone)
        messages.success(request,'New address added successfully')
        # new_address.save()
        return redirect('ecommapp:customer-dashboard')
    
    profile = profile_details.objects.get(user = request.user)
    print(profile)
        
    context = {'orders_list':orders_list, 
               'address':address , 
               'orders':orders, 
               'month':month, 
               'total_orders':total_orders, 
               'profile':profile
    }
    
    return render(request,'customer-dashboard.html',context)

def order_details(request, id):
    order = Cartorder.objects.get(user = request.user, id = id)
    products = CartorderItem.objects.filter(order = order)
    context = {'products':products}
    
    return render(request,'order-details.html',context)

def make_address_default(request):
    id = request.GET.get('id')
    Address.objects.update(status = False)
    Address.objects.filter(id = id).update(status = True)
    return JsonResponse({'bool':True})

def wishlist_view(request):
    try:
        Wishlist = whislist.objects.all()
    except:
        Wishlist = None
    return render(request,'wishlist.html',{'Wishlist':Wishlist})

def add_to_wishlist(request):
    id = request.GET.get('id')
    product = Product.objects.get(id = id)
    
    context = {}
    
    wishlist_count = whislist.objects.filter(user = request.user, product = product).count()
    if wishlist_count > 0:
        # whislist.objects.filter(user = request.user, product = product).delete()
        context = {
            "bool":True
        }
        
    else:
        new_wishlist = whislist.objects.create(user = request.user, product = product)
        context = {
            "bool":True        
        }
            
    return JsonResponse({'bool':True})

def remove_wishlist(request):
    pid = request.GET.get('id')
    Wishlist = whislist.objects.filter(user = request.user)
    Whislist_d = whislist.objects.get(id=pid)
    delete_product = Whislist_d.delete()
    
    context ={
        "bool":True,
        "wishlist":Wishlist
    }
    whislist_json = serializers.serialize('json',Wishlist)
    data = render_to_string('async/wishlist.html',context)
    return JsonResponse({"data":data, "w":whislist_json})


def contact_view(request):
    return render(request,'contact.html')

def ajax_contact(request):
    print("Data Accessed!!")
    if request.method == 'POST': 
        print("POST request received")  # Ensure POST method is called
       
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
            
        contact = contactus.objects.create(
            full_name = full_name, 
            phone = phone,
            email = email, 
            message = message, 
            subject = subject
        )
            
    context = {
        "bool":True,
        "messages":"Message sent successfully",
        # "new_contact":new_contact
    }
    
    return JsonResponse({"data":context})
