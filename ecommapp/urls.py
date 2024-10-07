from django.contrib import admin
from django.urls import path
from . import views

app_name = 'ecommapp'

urlpatterns = [
    path('',views.index,name="index"),
    path('products-list',views.product_list,name="products-list"),
    path('category-list',views.category_list,name="category-list"),
    path('category-list/<cid>/',views.category_product_list,name="category-product-list")
]
