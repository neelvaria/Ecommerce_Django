from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("",views.vendor_dashboard,name="dashboard"),
    path("products/",views.product_list,name="products"),
    path("addproduct/",views.add_product,name="addproduct"),
]
