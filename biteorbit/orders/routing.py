from django.urls import re_path

from . import consumers
from .consumers import (
    OrderConsumer,
    GPSConsumer,
    ChatConsumer,
    TrackingConsumer,
    OrderTrackingConsumer
)

websocket_urlpatterns = [ 
    
    re_path( 
        r'ws/orders/$', 
        OrderConsumer.as_asgi() 
    ), 
    
    re_path(
        r'ws/gps/$',
        GPSConsumer.as_asgi()
    ),
    
    re_path(
        r'ws/chat/(?P<order_id>\w+)/$',
        ChatConsumer.as_asgi()
    ),
    
    re_path(
        r"ws/tracking/(?P<order_id>\w+)/$",
        TrackingConsumer.as_asgi()
    ),
    
    re_path(
        r'ws/order/(?P<order_id>\d+)/$',
        OrderTrackingConsumer.as_asgi()
    ),
    
]