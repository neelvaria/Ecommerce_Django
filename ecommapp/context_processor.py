from ecommapp.models import *
from django.db.models import Min,Max
from django.contrib import messages

def defaults(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    
    min_max_price = Product.objects.aggregate(Min('price'),Max('price'))
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    
    try:
        whislist_count = whislist.objects.filter(user = request.user)
    except:
        messages.info(request,'You need login first to accessing to wishlist')
        whislist_count = 0
    
    
    return{
        'categories':categories,
        'add':address,
        'vendors':vendors,
        'min_max_price':min_max_price,
        'whislist_count':whislist_count
        
    }