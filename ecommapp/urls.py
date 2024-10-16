from django.contrib import admin
from django.urls import path , include
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
    
    #filter
    path('filter-product/',views.filter_product,name="filter-product"),
    
    #add to cart
    path('add-to-cart/',views.add_to_cart,name="add_to_cart"),
    path('cart/',views.cart_view,name="cart"),
    path('delete-from-cart/',views.delete_from_cart,name="delete-from-cart"),
    path('update-cart/',views.update_cart,name="update-cart"),
    
    #checkout
    path('checkout/',views.checkout_view,name="checkout"),
    
    #paypal 
    path('paypal/',include('paypal.standard.ipn.urls')),
    
    #payment success
    path('payment-success/',views.payment_completed_view,name="payment-success"),
    
    #payment failed
    path('payment-failed/',views.payment_failed_view,name="payment-failed"),
]
