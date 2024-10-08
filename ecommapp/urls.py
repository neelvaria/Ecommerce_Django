from django.contrib import admin
from django.urls import path
from . import views

app_name = 'ecommapp'

urlpatterns = [
    path('',views.index,name="index"),
    path('category-list',views.category_list,name="category-list"),
    path('category-list/<cid>/',views.category_product_list,name="category-product-list"),
    
    #Vendorlist
    path('vendor-list',views.vendor_list,name="vendor-list"),
    path('vendor-list/<v_id>/',views.vendor_details_view,name="vendor-details-list"),
    
    #Product
    path('products-list',views.product_list,name="products-list"),
    path('products-list/<p_id>/',views.product_details_view,name="product-details-list"),   

]
