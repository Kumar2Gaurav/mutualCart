from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework import views ,status
from rest_framework.response import Response
from .models import Cart, Product
import requests


# Create your views here.


class GetPostCart(ListCreateAPIView, views.APIView):


    def get(self, request):
        all_products,url = [None] * 2
        try:
            url = "https://api.jsonbin.io/b/603c78b081087a6a8b931ebb"
            all_products = {"status":True,"data":requests.get(url)}
            return Response(all_products, status=status.HTTP_404_NOT_FOUND)

        except:
            result ={"status":False,"data": "Unable to fetch result"}
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        finally:
            del all_products,url

    def post(self, request):
        try:
            msg = f"Post Request in GetPostDataType {request.data}"
            user_obj = request.user
            if user_obj.users.role == "super_admin":
                title = request.data.get("title")
                type = request.data.get("type")
                description = request.data.get("description")
                filename = request.data.get("filename")
                height = request.data.get("height")
                width = request.data.get("width")
                price = request.data.get("price")
                rating = request.data.get("rating")
                quantity = request.data.get("quantity")
                product_check = Product.objects.filter(title=title,type=type)
                if quantity < 0:
                    result = {"status": True, "data": "Quantity cant be less than 0"}
                    return Response(result, status=status.HTTP_200_OK)
                if product_check:
                    product_check.update(description=description,filename=filename,
                                         height=height,width=width,price=price,rating=rating)
                    product = product_check[0]
                else:
                    product = Product(title=title,type=type,description=description,filename=filename,
                                             height=height,width=width,price=price,rating=rating)
                    product.save()

                cart = Cart(product_map= product,product_count=quantity)
                cart.save()

                result = {"status": True, "data": "Product added into cart","cart_id":cart.id}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {"status": False, "data": "You are not  authorised to access"}
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        except:
            result = {"status": False, "data": "No Content"}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        try:
            cart_id = int(request.data.get("cart_id"))
            quantity = int(request.data.get("quantity"))
            if quantity < 0:
                result = {"status": True, "data": "Quantity cant be less than 0", "cart_id": cart_id}
                return Response(result, status=status.HTTP_200_OK)
            Cart.objects.filter(cart_id= cart_id).update(product_count=quantity)
            result = {"status": True, "data": "Product quantites changed", "cart_id": cart_id}
            return Response(result, status=status.HTTP_200_OK)
        except:
            result = {"status": False, "data": "You are not  authorised to access"}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            cart_id = int(request.data.get("cart_id"))
            Cart.objects.filter(cart_id= cart_id).delete()
            result = {"status": True, "data": "Product removed from cart", "cart_id": cart_id}
            return Response(result, status=status.HTTP_200_OK)
        except:
            result = {"status": False, "data": "You are not  authorised to access"}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)






