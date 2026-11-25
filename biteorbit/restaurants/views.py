from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Food
from .serializers import FoodSerializer

class FoodListView(APIView):

    def get(self, request, restaurant_id=None):

        if restaurant_id:
            foods = Food.objects.filter(restaurant_id=restaurant_id)
        else:
            foods = Food.objects.all()

        serializer = FoodSerializer(foods, many=True)

        return Response(serializer.data)