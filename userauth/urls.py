from django.contrib import admin
from django.urls import path
from . import views

app_name = 'userauth'

urlpatterns = [
    path('register',views.register_view,name="register"),
    path('login',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('profile_update',views.update_profile,name="profile_update"),
]