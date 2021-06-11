from django.urls import path
from views import GetPostCart


urlpatterns = [
    path("cart",GetPostCart.as_view(),name = "cart_system")
    ]