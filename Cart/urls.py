from django.urls import path
from .views import GetPostCart , login, signup


urlpatterns = [
    path("cart",GetPostCart.as_view(),name = "cart_system"),
    path("login", login,name = "login"),
    path("signup", signup,name = "signup")
    ]