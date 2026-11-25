from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse
from django.contrib.auth.models import User

from restaurants.models import Restaurant
from foods.models import Food
from orders.models import Order

import json

# ===================================
# ALL RESTAURANTS API
# ===================================

@api_view(['GET'])
def restaurants_api(request):

    restaurants = Restaurant.objects.all()

    data = []

    for restaurant in restaurants:

        data.append({

            "id": restaurant.id,

            "name": restaurant.name,

            "description": restaurant.description,

            "rating": restaurant.rating,

            "delivery_time": restaurant.delivery_time,

            "image":
                request.build_absolute_uri(
                    restaurant.image.url
                ) if restaurant.image else ""

        })

    return JsonResponse(data, safe=False)


# ===================================
# SINGLE RESTAURANT API
# ===================================

@api_view(['GET'])
def single_restaurant_api(request, id):

    try:

        restaurant = Restaurant.objects.get(id=id)

        data = {

            "id": restaurant.id,

            "name": restaurant.name,

            "description": restaurant.description,

            "rating": restaurant.rating,

            "delivery_time": restaurant.delivery_time,

            "image":
                request.build_absolute_uri(
                    restaurant.image.url
                ) if restaurant.image else ""

        }

        return JsonResponse(data, safe=False)

    except Restaurant.DoesNotExist:

        return JsonResponse({
            "error": "Restaurant not found"
        })


# ===================================
# RESTAURANT FOODS API
# ===================================

@api_view(['GET'])
def restaurant_foods_api(request, restaurant_id):

    foods = Food.objects.filter(
        restaurant_id=restaurant_id
    )

    data = []

    for food in foods:

        data.append({

            "id": food.id,

            "name": food.name,

            "description": food.description,

            "price": food.price,

            "image":
                request.build_absolute_uri(
                    food.image.url
                ) if food.image else ""

        })

    return JsonResponse(data, safe=False)


# ===================================
# CREATE ORDER API
# ===================================

@api_view(['POST'])
def create_order_api(request):

    try:

        data = request.data

        order = Order.objects.create(

            user=request.user,

            customer_name=data.get('customer_name'),

            mobile=data.get('mobile'),

            address=data.get('address'),

            city=data.get('city'),

            pincode=data.get('pincode'),

            payment_method=data.get('payment_method'),

            total_price=data.get('total_price'),

            
        )

        return Response({

            "success": True,

            "message":
                "Order placed successfully",

            "order_id": order.id

        })

    except Exception as e:

        return Response({

            "success": False,

            "error": str(e)

        })


# ===================================
# REGISTER API
# ===================================

@api_view(['POST'])
def register_api(request):

    username = request.data.get("username")

    email = request.data.get("email")

    password = request.data.get("password")

    if User.objects.filter(
        username=username
    ).exists():

        return Response({
            "error": "Username already exists"
        })

    User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({
        "message": "User Registered Successfully"
    })