from django.contrib import admin
from ecommapp.models import *
# Register your models here.

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['user','title','product_image','price','category','vendor','featured','product_status','p_id']
admin.site.register(Product,ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']
admin.site.register(Category,CategoryAdmin)
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image','contact','address']
admin.site.register(Vendor,VendorAdmin)

class CartorderAdmin(admin.ModelAdmin):
    list_display = ['user','price','paid_status','order_date','product_status']
admin.site.register(Cartorder,CartorderAdmin)

class CartorderitemAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no','product_status','item','image','qty','price','total']
admin.site.register(CartorderItem,CartorderitemAdmin)

class ProductreviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating','date']
admin.site.register(product_review,ProductreviewAdmin)
    
class whislistAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']
admin.site.register(whislist,whislistAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','address','status']
admin.site.register(Address,AddressAdmin)

class Product_imageAdmin(admin.ModelAdmin):
    list_display = ['product','images']
admin.site.register(ProductImage,Product_imageAdmin)
    
