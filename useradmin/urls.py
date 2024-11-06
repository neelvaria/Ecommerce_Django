from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("",views.vendor_dashboard,name="dashboard"),
    path("products/",views.product_list,name="products"),
    path("addproduct/",views.add_product,name="addproduct"),
    path("editproduct/<int:pid>/",views.update_product,name="editproduct"),
    path("deleteproduct/<int:pid>/",views.delete_product,name="deleteproduct"),
    path("orders/",views.orders,name="orders"),
    path("orderdetails/<str:id>/",views.order_details,name="orderdetails"),
    path("change_order_status/<str:oid>/",views.change_order_status,name="change_order_status"),
    path("shop/",views.shop_page,name="shop"),
    path("reviews/",views.reviews,name="reviews"),
    path("settings/",views.settings,name="settings"),
    path("changepassword/",views.change_password,name="changepassword"),
]
