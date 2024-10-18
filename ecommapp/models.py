from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from userauth.models import User 
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
STATUS_CHOICES = (
    ("process","Process"),
    ("shipped","Shipped"),
    ("delivered","Delivered"), 
)

STATUS = (
    ("disabled","Disabled"), 
    ("published","Published"),
    ("in_review","In Review"),
    ("completed","Completed"),
    ("rejected","Rejected"),
)

RATING = (
    ("1","⭐☆☆☆☆"),
    ("2","⭐⭐☆☆☆"),
    ("3","⭐⭐⭐☆☆"),
    ("4","⭐⭐⭐⭐☆"),
    ("5","⭐⭐⭐⭐⭐"),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    c_id = ShortUUIDField(unique=True,max_length=25,prefix="cat",alphabet="abcdefjh12345")
    title = models.CharField(max_length=100,default="Category Title")
    image = models.ImageField(upload_to="category",default="category/default.png")
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def category_image(self):
        return mark_safe('<img src="{}" width="50" />'.format(self.image.url))
    
    def __str__(self):
        return self.title
    
class tags(models.Model):
    pass

class Vendor(models.Model):
    v_id = ShortUUIDField(unique=True,length=10,max_length=15,prefix="ven",alphabet="abcdefjh12345")
    
    title = models.CharField(max_length=100,default="Vendor Title")
    image = models.ImageField(upload_to=user_directory_path,default="vendor/default.png")
    cover_image = models.ImageField(upload_to=user_directory_path,default="vendor/default.png")
    description = RichTextUploadingField(null=True,blank=True, default="Vendor Description")
    # description = models.TextField(null=True,blank=True, default="Vendor Description")
    
    address = models.CharField(max_length=100,default="123 Main Street, San Francisco, CA 94111")
    contact = models.CharField(max_length=100,default="123-456-7890")
    chat_resp_time = models.CharField(max_length=100,default="24 hours")
    shipping_time = models.CharField(max_length=100,default="3 days")
    authetic_rating = models.CharField(max_length=100,default="4.5")
    day_return = models.CharField(max_length=100,default="Yes")
    warranty_period = models.CharField(max_length=100,default="Yes")
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True) 
    
    class Meta:
        verbose_name_plural = "Vendor"
    
    def vendor_image(self):
        return mark_safe('<img src="{}" width="50" />'.format(self.image.url))
    
    def __str__(self):
        return self.title

class Product(models.Model):
    p_id = ShortUUIDField(unique=True,length=10,max_length=15,alphabet="abcdefjh12345")
    
    title = models.CharField(max_length=100, default="Product Title")
    image = models.ImageField(upload_to=user_directory_path)
    description = RichTextUploadingField(null=True,blank=True, default="Product Description")  
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default=1.99)
    old_price = models.DecimalField(max_digits=9999999999, decimal_places=2, default=2.99)
    
    # specification = models.TextField(null=True,blank=True) 
    specification = RichTextUploadingField(null=True,blank=True) 

    type = models.CharField(max_length=100, default="organic",null=True,blank=True)
    stock = models.CharField(max_length=100, default="0",null=True,blank=True)
    expiry = models.CharField(max_length=100, default="10 Days",null=True,blank=True)
    mfg = models.DateTimeField(auto_now_add=False,blank=True,null=True)

    
    tags = TaggableManager(blank=True)
    product_status = models.CharField(choices=STATUS, max_length=100, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="category") 
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True, related_name="products") 
    
    sku = ShortUUIDField(unique=True,length=4,max_length=10,alphabet="abcdefjh12345",prefix="sku")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Products"
    
    def product_image(self):
        return mark_safe('<img src="{}" width="50" />'.format(self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price
    
class ProductImage(models.Model):
    images = models.ImageField(upload_to="product_images",default="product_images/default.png")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True, related_name="p_image")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Image"
    

#####################Cart , Order , Order Item #####################

class Cartorder(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default=1.99)
    paid_status = models.BooleanField(default=False) 
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default="Process")
    
    class Meta:
        verbose_name_plural = "Cart Orders"
    
class CartorderItem(models.Model):
    order = models.ForeignKey(Cartorder,on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default=1.99)
    total = models.DecimalField(max_digits=9999999999, decimal_places=2, default=1.99)
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
        
    def order_image(self):
        return mark_safe('<img src="{/media/}" width="50" />'.format(self.image))

##################### Product Review, wishlist, Address #####################

class product_review(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="reviews")
    review = models.TextField()
    rating = models.CharField(choices=RATING, default=None,max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Review"
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating

class whislist(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlist"
    
    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=1000, null=True)
    status = models.BooleanField(default=False)
    contact = models.CharField(max_length=200, null=True)
    
    class Meta:
        verbose_name_plural = "Address"
    
    def __str__(self):
        return self.address

