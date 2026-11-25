from django.urls import path
from .views import *

urlpatterns = [

    path('restaurants/', RestaurantListView.as_view()),
    path('restaurants/<int:id>/', RestaurantDetailView.as_view()),

    path('restaurants/<int:restaurant_id>/foods/', FoodListView.as_view()),

    # NEW URL
    path('foods/', FoodListView.as_view()),

    path('orders/', OrderCreateView.as_view()),

]