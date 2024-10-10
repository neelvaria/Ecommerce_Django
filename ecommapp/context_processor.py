from ecommapp.models import *

def defaults(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
        
    return{
        'categories':categories,
        'add':address,
        'vendors':vendors
    }