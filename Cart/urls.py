from django.urls import path
from .views import GetPostCart , login


urlpatterns = [
    path("cart",GetPostCart.as_view(),name = "cart_system"),
    path("login/", login,name = "login")
    ]