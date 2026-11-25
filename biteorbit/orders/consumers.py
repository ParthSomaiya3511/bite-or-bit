import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

from .models import Order


# =========================================
# ORDER CONSUMER
# =========================================

class OrderConsumer(

    AsyncWebsocketConsumer
):

    async def connect(self):

        self.room_group_name = "orders"

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name
        )

        await self.accept()

    async def disconnect(

        self,

        close_code
    ):

        await self.channel_layer.group_discard(

            self.room_group_name,

            self.channel_name
        )

    async def receive(

        self,

        text_data
    ):

        pass

    # SEND ORDER

    async def send_order(self, event):

        await self.send(

            text_data=json.dumps({

                "type": "new_order",

                "order": event["order"]
            })
        )



# =========================================
# GPS CONSUMER
# =========================================

class GPSConsumer(

    AsyncWebsocketConsumer
):

    async def connect(self):

        self.room_group_name = "gps"

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name
        )

        await self.accept()

    async def disconnect(

        self,

        close_code
    ):

        await self.channel_layer.group_discard(

            self.room_group_name,

            self.channel_name
        )

    async def receive(

        self,

        text_data
    ):

        data = json.loads(text_data)

        # BROADCAST GPS

        await self.channel_layer.group_send(

            self.room_group_name,

            {

                "type":
                    "send_gps",

                "latitude":
                    data["latitude"],

                "longitude":
                    data["longitude"]
            }
        )

    async def send_gps(self, event):

        await self.send(

            text_data=json.dumps({

                "latitude":
                    event["latitude"],

                "longitude":
                    event["longitude"]
            })
        )



# =========================================
# CHAT CONSUMER
# =========================================

class ChatConsumer(

    AsyncWebsocketConsumer
):

    async def connect(self):

        self.room_name = self.scope[
            'url_route'
        ]['kwargs']['order_id']

        self.room_group_name = (

            f"chat_{self.room_name}"
        )

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name
        )

        await self.accept()

    async def disconnect(

        self,

        close_code
    ):

        await self.channel_layer.group_discard(

            self.room_group_name,

            self.channel_name
        )

    async def receive(

        self,

        text_data
    ):

        data = json.loads(text_data)

        message = data["message"]

        sender = data["sender"]

        await self.channel_layer.group_send(

            self.room_group_name,

            {

                "type":
                    "chat_message",

                "message":
                    message,

                "sender":
                    sender
            }
        )

    async def chat_message(

        self,

        event
    ):

        await self.send(

            text_data=json.dumps({

                "message":
                    event["message"],

                "sender":
                    event["sender"]
            })
        )
        
        

class TrackingConsumer(
    AsyncWebsocketConsumer
):

    async def connect(self):

        self.order_id = self.scope[
            "url_route"
        ]["kwargs"]["order_id"]

        self.room_group_name = (
            f"tracking_{self.order_id}"
        )

        await self.channel_layer.group_add(

            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(
        self,
        close_code
    ):

        await self.channel_layer.group_discard(

            self.room_group_name,
            self.channel_name
        )

    async def receive(
        self,
        text_data
    ):

        data = json.loads(text_data)

        lat = data["lat"]

        lng = data["lng"]

        await self.save_location(
            lat,
            lng
        )

        await self.channel_layer.group_send(

            self.room_group_name,

            {

                "type": "send_location",

                "lat": lat,

                "lng": lng
            }
        )

    async def send_location(
        self,
        event
    ):

        await self.send(

            text_data=json.dumps({

                "lat": event["lat"],

                "lng": event["lng"]
            })
        )

    @sync_to_async
    def save_location(
        self,
        lat,
        lng
    ):

        order = Order.objects.get(
            id=self.order_id
        )

        order.rider_lat = lat

        order.rider_lng = lng

        order.save()
        
        
class OrderTrackingConsumer(

    AsyncWebsocketConsumer
):

    async def connect(self):

        self.order_id = self.scope[

            "url_route"

        ]["kwargs"]["order_id"]

        self.room_group_name = (

            f"order_{self.order_id}"
        )

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name
        )

        await self.accept()

    async def disconnect(

        self,

        close_code
    ):

        await self.channel_layer.group_discard(

            self.room_group_name,

            self.channel_name
        )

    async def order_update(

        self,

        event
    ):

        await self.send(

            text_data=json.dumps(

                event["data"]
            )
        )