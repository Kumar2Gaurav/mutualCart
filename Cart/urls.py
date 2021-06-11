from django.urls import path
from .views import GetPostCart , login, signup,user_cart_list


urlpatterns = [
    path("cart",GetPostCart.as_view(),name = "cart_system"),
    path("user_cart_list" , user_cart_list,name = "user_cart_list"),
    path("login", login,name = "login"),
    path("signup", signup,name = "signup")
    ]