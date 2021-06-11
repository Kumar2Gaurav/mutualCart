from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework import views ,status
from rest_framework.response import Response
from .models import Cart, Product
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login

import requests

def checkuser(request):
    token = request.headers["Authorization"].split()[1]
    token_check = Token.objects.filter(key=token)
    if token_check:
        return True
    return False




# Create your views here.

def create_user(username, email, firstname, lastname, password=None):
    try:
        user_check  = User.objects.filter(username=username,email=email)
        if user_check:
            return False
        user_obj = User.objects.create(username=username, email=email, first_name=firstname
                                       , last_name=lastname)
        if password:
            user_obj.set_password(password)
            user_obj.save()
        else:
            default_password = "password@123"
            user_obj.set_password(default_password)
            user_obj.save()
        return  True
    except:
        return False



@api_view(['POST'])
def signup(request):
    username = request.data.get("username")
    email = request.data.get("email")
    firstname = request.data.get("firstname")
    lastname = request.data.get("lastname")
    password = request.data.get("password",None)
    user_creation = create_user(username, email, firstname, lastname, password)
    if user_creation:
        result = {"status":True,"data":"User created Successfully"}
        return Response(result,status.HTTP_200_OK)
    else:
        result = {"status":False,"data":"Unable to create User"}
        return Response(result,status.HTTP_200_OK)



@api_view(['GET'])
def login(request):
    try:
        username = request.GET.get("username")
        password = request.GET.get("password")
        user_obj = authenticate(username=username,password=password)
        if user_obj:
            user_obj = user_obj
            token, created = Token.objects.get_or_create(user=user_obj)
            result = {"status":False,"data":"User tokem generated","token":token.key}
            return Response(result,status.HTTP_404_NOT_FOUND)
        else:
            result = {"status":False,"data":"User not found please sign up"}
            return Response(result,status.HTTP_404_NOT_FOUND)
    except:
        result = {"status": False, "data": "Request Error"}
        return Response(result, status.HTTP_400_BAD_REQUEST)
    


class GetPostCart(ListCreateAPIView, views.APIView):


    def get(self, request):
        all_products,url = [None] * 2
        try:
            import ipdb;ipdb.set_trace()
            if checkuser(request):
                url = "https://api.jsonbin.io/b/603c78b081087a6a8b931ebb"
                all_products = {"status":True,"data":requests.get(url)}
                return Response(all_products, status=status.HTTP_200_OK)
            else:
                result = {"status": False, "data": "You are not  authorised to access"}
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)

        except:
            result ={"status":False,"data": "Unable to fetch result"}
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        finally:
            del all_products,url

    def post(self, request):
        try:
            msg = f"Post Request in GetPostDataType {request.data}"
            if checkuser(request):
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
            if checkuser(request):
                cart_id = int(request.data.get("cart_id"))
                quantity = int(request.data.get("quantity"))
                if quantity < 0:
                    result = {"status": True, "data": "Quantity cant be less than 0", "cart_id": cart_id}
                    return Response(result, status=status.HTTP_200_OK)
                Cart.objects.filter(cart_id= cart_id).update(product_count=quantity)
                result = {"status": True, "data": "Product quantites changed", "cart_id": cart_id}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {"status": False, "data": "You are not  authorised to access"}
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        except:
            result = {"status": False, "data": "You are not  authorised to access"}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            if checkuser(request):
                cart_id = int(request.data.get("cart_id"))
                Cart.objects.filter(cart_id= cart_id).delete()
                result = {"status": True, "data": "Product removed from cart", "cart_id": cart_id}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {"status": False, "data": "You are not  authorised to access"}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except:
            result = {"status": False, "data": "You are not  authorised to access"}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)






