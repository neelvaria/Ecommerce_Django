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
    
    #Tags
    path('products/tag/<slug:tag_slug>/',views.tags_list,name="tags"),
    
    #reviews
    path('ajax_add_review/<int:p_id>/',views.ajax_add_review,name="ajax_add_review"),
    
    #Search
    path('search/',views.search_view,name="search"),
]
