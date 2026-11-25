from django.contrib import admin
from django.urls import path, include

from users.views import register_user, login_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import (
    restaurants_api,
    single_restaurant_api,
    restaurant_foods_api,
    create_order_api,
    register_api
)

urlpatterns = [

    # ALL RESTAURANTS
    path(
        'restaurants/',
        restaurants_api
    ),

    # SINGLE RESTAURANT
    path(
        'restaurants/<int:id>/',
        single_restaurant_api
    ),

    # RESTAURANT FOODS
    path(
        'restaurants/<int:restaurant_id>/foods/',
        restaurant_foods_api
    ),

    # ORDERS
    path(
        'orders/',
        create_order_api
    ),

    # REGISTER
    path(
        'register/',
        register_api
    ),

    # LOGIN JWT
    path(
        'login/',
        TokenObtainPairView.as_view()
    ),

    # REFRESH TOKEN
    path(
        'token/refresh/',
        TokenRefreshView.as_view()
    ),
    
    path('register/', register_user),

    path('login/', login_user),

]