from ecommapp.models import *

def defaults(request):
    categories = Category.objects.all()
    address = Address.objects.get(user=request.user)
    return{
        'categories':categories,
        'add':address
    }