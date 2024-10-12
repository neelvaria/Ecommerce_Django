from ecommapp.models import *
from django.db.models import Min,Max

def defaults(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    
    min_max_price = Product.objects.aggregate(Min('price'),Max('price'))
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
        
    return{
        'categories':categories,
        'add':address,
        'vendors':vendors,
        'min_max_price':min_max_price
    }