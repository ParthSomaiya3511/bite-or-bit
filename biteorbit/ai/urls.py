from django.urls import path
from .views import DeliveryAIAPIView

urlpatterns = [

    path(
        "delivery-assistant/",
        DeliveryAIAPIView.as_view()
    ),
]