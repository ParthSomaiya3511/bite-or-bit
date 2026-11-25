# 

import math
import random
import razorpay
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from reportlab.pdfgen import canvas

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from django.conf import settings
from .payment_utils import *
from .models import Order, OrderItem , Payment, DeliveryLocation, Rider, ChatMessage, RiderSOS, Restaurant, RestaurantOwner, Food, PaymentTransaction, CustomerWallet, WalletTransaction, MembershipPlan, CustomerMembership, Coupon, CashbackTransaction, CustomerDevice, CustomerNotification, CustomerProfile, CustomerAddress, SupportTicket, SupportMessage, CustomerFeedback
from .serializers import OrderSerializer, DeliveryLocationSerializer, RiderSerializer, RiderSOSSerializer, RestaurantSerializer, RestaurantOwnerSerializer, FoodSerializer, CustomerWalletSerializer, WalletTransactionSerializer, MembershipPlanSerializer, CustomerMembershipSerializer, CouponSerializer, CustomerNotificationSerializer, CustomerProfileSerializer, CustomerAddressSerializer, SupportTicketSerializer, SupportMessageSerializer, CustomerFeedbackSerializer
from django.shortcuts import get_object_or_404

from reportlab.lib import colors
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus.tables import Table, TableStyle

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

from django.db.models import Sum
from django.db.models import Count
from django.db.models import Avg
from django.utils.timezone import now
from datetime import timedelta

from django.db.models.functions import TruncMonth

from .utils.eta import (
    calculate_distance,
    calculate_eta
)

from rest_framework.parsers import ( 
    MultiPartParser, 
    FormParser 
)

from .utils.route_optimizer import (
    find_best_rider
)

from .utils.cluster import (
    find_cluster_orders
)

from .utils.priority import (
    calculate_priority
)

from .utils.auto_assign import (
    auto_assign_rider
)

from .utils.heatmap import (
    generate_heatmap
)

from .utils.order_batching import (
    create_order_batches
)

from .utils.predictive_demand import (
    predict_delivery_demand
)

from .utils.rider_analytics import (
    rider_performance_analytics
)

from .utils.fraud_detection import (
    detect_fraud
)


from .utils.smart_eta import (
    smart_delivery_eta
)


from .utils.traffic_ai import (
    simulate_traffic
)

from .utils.weather_ai import (
    weather_delivery_ai
)

from .utils.rider_wallet import (
    update_rider_wallet
)

from .utils.withdraw_ai import (
    withdraw_ai_check
)

from .utils.incentive_ai import (
    apply_rider_bonus
)

from .utils.leaderboard_ai import (
    update_rider_performance
)

from .utils.achievement_ai import (
    unlock_rider_achievement
)

from .utils.mission_ai import (

    create_daily_missions,
    update_missions
)

from .utils.streak_ai import (
    update_rider_streak
)

from .utils.discipline_ai import (
    update_rider_discipline
)

from .utils.attendance_ai import (

    rider_clock_in,
    rider_clock_out
)

from .utils.smart_scheduler import (

    generate_rider_schedule,
    get_best_scheduled_rider
)

from .utils.fatigue_detector import (
    detect_rider_fatigue
)

from .utils.rider_mood_ai import (
    detect_rider_mood
)

from .utils.rider_safety_ai import (
    detect_rider_safety
)

from ai_engine.traffic_ai import (
    calculate_ai_eta
)

from ai_engine.dynamic_pricing import (
    calculate_dynamic_price
)

from ai_engine.referral_engine import (
    generate_referral_code
)

from ai_engine.reward_engine import (
    calculate_rewards
)

from ai_engine.recommendation_engine import (
    recommend_foods
)

from channels.layers import (

    get_channel_layer
)

from asgiref.sync import (

    async_to_sync
)

from ai_engine.multi_city import get_best_city_rider

@api_view(["POST"])
@permission_classes([IsAuthenticated])

def create_order(request):
    
    # =========================================
# FIREBASE PUSH NOTIFICATION
# =========================================

    def send_push_notification(

        token,
        title,
        body
    ):

        FIREBASE_SERVER_KEY = "BP9UyIvQzNKzFmG3eanO_BxVkXw89tuofbjzuFmG3lFNGYqacCg9ASFnZPO6Vnt09Wfebk6E2m-jcdZ9GA-dtKU"

        headers = {

            "Authorization":
                f"key={FIREBASE_SERVER_KEY}",

            "Content-Type":
                "application/json"
        }

        payload = {

            "to": token,

            "notification": {

                "title": title,

                "body": body,

                "sound": "default"
            }
        }

        try:

            response = requests.post(

                "https://fcm.googleapis.com/fcm/send",

                json=payload,

                headers=headers
            )

            print(response.json())

        except Exception as e:

            print(e)

    try:

        data = request.data

        order = Order.objects.create(

            user=request.user,

            customer_name=data.get("customer_name"),

            mobile=data.get("mobile"),

            address=data.get("address"),

            city=data.get("city"),

            pincode=data.get("pincode"),

            payment_method=data.get("payment_method"),

            total_price=data.get("total_price"),
            
            fcm_token=data.get("fcm_token"),
            
            rider=best_rider,

            eta_minutes=int(eta),


        )
        
        if best_rider:

            best_rider.is_busy = True

            best_rider.save()

        
        DeliveryLocation.objects.create(

            order=order,

            latitude=23.0300,

            longitude=72.5800
        )
        
        available_riders = Rider.objects.filter(

            is_available=True
        )

        nearest_rider = None

        minimum_distance = 999999

        customer_lat = 23.0225
        customer_lng = 72.5714

        for rider in available_riders:

            distance = calculate_distance(

                customer_lat,
                customer_lng,

                rider.latitude,
                rider.longitude
            )

            if distance < minimum_distance:

                minimum_distance = distance

                nearest_rider = rider

        # ASSIGN RIDER

        if nearest_rider:

            order.assigned_rider = nearest_rider

            order.save()
            
            # =========================================
            # LIVE WEBSOCKET EVENT
            # =========================================

            channel_layer = get_channel_layer()

            async_to_sync(

                channel_layer.group_send

            )(

                "orders",

                {

                    "type": "send_order",

                    "order": {

                        "id": order.id,

                        "customer":
                            order.customer_name,

                        "amount":
                            str(order.total_price),

                        "status":
                            order.status
                    }
                }
            )


            nearest_rider.is_available = False

            nearest_rider.save()

            DeliveryLocation.objects.update_or_create(

                order=order,

                defaults={

                    "latitude": nearest_rider.latitude,
                    "longitude": nearest_rider.longitude
                }
            )
        

        items = data.get("items", [])

        for item in items:

            OrderItem.objects.create(

                order=order,

                food_name=item.get("name"),

                price=item.get("price"),

                quantity=item.get("quantity", 1),

                image=item.get("image", "")

            )
            

        return Response({

            "success": True,

            "order_id": order.id,

            "message": "Order placed successfully",
            
            "cluster_id": cluster_id,

        })

    except Exception as e:

        return Response({

            "success": False,

            "error": str(e)

        })
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])

def order_history(request):

    user = request.user

    orders = Order.objects.filter(
        customer_name=user.username
    ).order_by("-id")

    data = []

    for order in orders:

        items = []

        for item in order.items.all():

            items.append({

                "food_name": item.food_name,
                "price": item.price,
                "quantity": item.quantity,
                "image": item.image

            })

        data.append({

            "id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "created_at": order.created_at,
            "items": items

        })

    return Response(data)


client = razorpay.Client( 
    auth=( 
        settings.RAZORPAY_KEY_ID, 
        settings.RAZORPAY_KEY_SECRET 
    )     
) 


@api_view(["POST"])
def create_payment(request):

    amount = int(request.data["amount"]) * 100

    order_id = request.data.get("order_id")

    order = Order.objects.get(id=order_id)

    razorpay_order = client.order.create({

        "amount": amount,
        "currency": "INR",
        "payment_capture": 1

    })

    # SAVE PAYMENT
    payment = Payment.objects.create(

        order=order,

        razorpay_order_id=razorpay_order["id"],

        amount=amount / 100,

        status="Pending"

    )

    return Response({

        "success": True,

        "key": settings.RAZORPAY_KEY_ID,

        "amount": amount,

        "razorpay_order_id":
            razorpay_order["id"]

    })



@api_view(["POST"])

def verify_payment(request):

    client = razorpay.Client(auth=(

        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET

    ))

    data = request.data

    params_dict = {

        'razorpay_order_id': data.get('razorpay_order_id'),

        'razorpay_payment_id': data.get('razorpay_payment_id'),

        'razorpay_signature': data.get('razorpay_signature')

    }

    try:

        client.utility.verify_payment_signature(params_dict)

        payment = Payment.objects.get(

            razorpay_order_id=data.get(
                'razorpay_order_id'
            )
        )

        payment.razorpay_payment_id = data.get(
            'razorpay_payment_id'
        )

        payment.razorpay_signature = data.get(
            'razorpay_signature'
        )

        payment.status = "Paid"

        payment.save()

        # AUTO ORDER CONFIRM
        order = payment.order

        order.status = "Confirmed"

        order.save()

        return Response({

            "success": True,
            "message": "Payment Successful"

        })

    except Exception as e:

        return Response({

            "success": False,
            "error": str(e)

        })
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])

def generate_invoice(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'attachment; filename="invoice_{order_id}.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<font size=24><b>BiteOrbit Invoice</b></font>",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    info = f"""
    <b>Order ID:</b> {order.id}<br/>
    <b>Customer:</b> {order.customer_name}<br/>
    <b>Status:</b> {order.status}<br/>
    <b>Total:</b> ₹{order.total_price}<br/>
    """

    elements.append(
        Paragraph(info, styles['BodyText'])
    )

    elements.append(Spacer(1, 20))

    data = [["Food", "Qty", "Price"]]

    for item in order.items.all():

        data.append([

            item.food_name,

            str(item.quantity),

            f"₹{item.price}"

        ])

    table = Table(data, colWidths=[250,100,100])

    table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00C9A7")),

        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8f8f8"))

    ]))

    elements.append(table)

    elements.append(Spacer(1, 30))

    thank = Paragraph(

        "<b>Thank you for ordering with BiteOrbit ❤️</b>",

        styles['Heading3']

    )

    elements.append(thank)

    doc.build(elements)

    return response


@api_view(["GET"]) 
@permission_classes([IsAuthenticated]) 

def user_orders(request): 
    orders = Order.objects.filter( 
        user=request.user 
    ).order_by("-created_at") 
    
    serializer = OrderSerializer( 
        orders, 
        many=True 
    ) 
    
    return Response(serializer.data)


class AdminOrdersView(APIView):

    def get(self, request):

        orders = Order.objects.all().order_by("-id")

        serializer = OrderSerializer(

            orders,
            many=True
        )

        return Response(serializer.data)



class UpdateOrderStatusView(APIView):

    def put(self, request, id):

        order = Order.objects.get(id=id)

        order.status = request.data.get("status")

        wallet_data = None

        if status == "Delivered":

            if order.assigned_rider:

                wallet_data = update_rider_wallet(

                    order.assigned_rider,

                    order.total_price
                )
                
                bonus_data = apply_rider_bonus(

                    order.assigned_rider,

                    order.assigned_rider.wallet.completed_orders
                )
   
                leaderboard_data = update_rider_performance(

                    order.assigned_rider,

                    order.eta_minutes,

                    True
                )
                    

                performance = RiderPerformance.objects.get(

                    rider=order.assigned_rider
                )

                achievement_data = unlock_rider_achievement(

                    order.assigned_rider,
                    performance
                )
                
                mission_data = update_missions(

                    order.assigned_rider
                )
                

                streak_data = update_rider_streak(

                    order.assigned_rider
                )
                

                late_delivery = False

                if order.eta_minutes > 30:

                    late_delivery = True

                discipline_data = update_rider_discipline(

                    order.assigned_rider,

                    late_delivery=late_delivery,

                    fraud=order.is_fraud
                )


        order.save()
        
        # =====================================
        # DELIVERY NOTIFICATION
        # =====================================

        CustomerNotification.objects.create(

            customer_mobile=

            order.mobile,

            title="Order Delivered",

            message=

            "Your food has been delivered."
        )

        # WEBSOCKET

        channel_layer = get_channel_layer()

        async_to_sync(
            channel_layer.group_send
        )(
            f"order_{order.id}",

            {

                "type":
                    "order_status_update",

                "status":
                    order.status
            }
        )

        # PUSH NOTIFICATION

        if order.fcm_token:

            send_push_notification(

                order.fcm_token,

                "Order Status Updated",

                f"Your order is now {order.status}"
            )

        return Response({
            

            "wallet_data": wallet_data,
            
            "bonus_data": bonus_data,
            
            "leaderboard_data": leaderboard_data,
            
            "achievement_data": achievement_data,
            
            "mission_data": mission_data,
            
            "streak_data": streak_data,
            
            "discipline_data": discipline_data,

            "success": True
        })
        
        
class TrackOrderView(APIView):

    def get(self, request, id):

        try:

            order = Order.objects.get(
                id=id
            )

            return Response({

                "success": True,

                "order_id":
                order.id,

                "status":
                order.status,

                "eta_minutes":
                order.eta_minutes,

                "customer_name":
                order.customer_name,

                "customer_mobile":
                order.customer_mobile,

                "address":
                order.address,

                "latitude":
                order.latitude,

                "longitude":
                order.longitude,

                # =====================================
                # RIDER DETAILS
                # =====================================

                "rider": {

                    "id":

                    order.rider.id

                    if order.rider else None,

                    "name":

                    order.rider.name

                    if order.rider else "No Rider",

                    "mobile":

                    order.rider.mobile

                    if order.rider else "",

                    "latitude":

                    order.rider.latitude

                    if order.rider else 0,

                    "longitude":

                    order.rider.longitude

                    if order.rider else 0
                }
            })

        except Exception as e:

            return Response({

                "success": False,

                "message":
                str(e)
            })

            
            
# =========================================
# CREATE PAYMENT ORDER
# =========================================

class CreatePaymentView(APIView):

    def post(self, request):

        try:

            order_id = request.data.get(

                "order_id"
            )

            order = Order.objects.get(

                id=order_id
            )

            amount = int(

                float(order.total_price) * 100
            )

            # =====================================
            # CREATE RAZORPAY ORDER
            # =====================================

            payment_order = client.order.create({

                "amount": amount,

                "currency": "INR",

                "payment_capture": 1
            })

            # =====================================
            # SAVE TRANSACTION
            # =====================================

            transaction = PaymentTransaction.objects.create(

                order=order,

                amount=order.total_price,

                razorpay_order_id=

                payment_order["id"],

                status="Created"
            )

            # =====================================
            # RESPONSE
            # =====================================

            return Response({

                "success": True,

                "payment": {

                    "razorpay_order_id":

                    payment_order["id"],

                    "amount": amount,

                    "currency": "INR",

                    "key":

                    settings.RAZORPAY_KEY_ID
                }
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })

        
# =========================================
# VERIFY PAYMENT
# =========================================

class VerifyPaymentView(APIView):

    def post(self, request):

        try:

            razorpay_order_id = request.data.get(

                "razorpay_order_id"
            )

            razorpay_payment_id = request.data.get(

                "razorpay_payment_id"
            )

            razorpay_signature = request.data.get(

                "razorpay_signature"
            )

            # =====================================
            # VERIFY SIGNATURE
            # =====================================

            client.utility.verify_payment_signature({

                'razorpay_order_id':

                razorpay_order_id,

                'razorpay_payment_id':

                razorpay_payment_id,

                'razorpay_signature':

                razorpay_signature
            })

            # =====================================
            # GET PAYMENT
            # =====================================

            payment = PaymentTransaction.objects.get(

                razorpay_order_id=

                razorpay_order_id
            )

            # =====================================
            # UPDATE PAYMENT
            # =====================================

            payment.payment_id = razorpay_payment_id

            payment.razorpay_signature = razorpay_signature

            payment.status = "Paid"
            
            device = CustomerDevice.objects.filter(

                customer_mobile=

                order.mobile

            ).first()

            if device:

                send_push_notification(

                    device.fcm_token,

                    "Payment Successful",

                    "Your payment was successful."
                )

            payment.save()

            # =====================================
            # UPDATE ORDER
            # =====================================

            order = payment.order

            order.payment_method = "Online"

            order.payment_status = "Paid"

            order.status = "Preparing"

            order.save()

            # =====================================
            # PAYMENT NOTIFICATION
            # =====================================

            CustomerNotification.objects.create(

                customer_mobile=

                payment.order.mobile,

                title="Payment Successful",

                message=

                f"Payment received for Order #{payment.order.id}"
            )

            wallet = CustomerWallet.objects.get(

                customer_mobile=order.mobile
            )

            reward_data = calculate_rewards(

                float(order.total_price),

                wallet.membership_plan
            )

            cashback = reward_data["cashback"]

            reward_points = reward_data["reward_points"]

            # =====================================
            # UPDATE WALLET
            # =====================================

            wallet.balance += cashback

            wallet.reward_points += reward_points

            wallet.total_cashback_earned += cashback

            # =====================================
            # VIP LEVEL SYSTEM
            # =====================================

            if wallet.reward_points >= 5000:

                wallet.vip_level = "Platinum"

            elif wallet.reward_points >= 2000:

                wallet.vip_level = "Gold"

            elif wallet.reward_points >= 500:

                wallet.vip_level = "Silver"

            wallet.save()

            # =====================================
            # SAVE CASHBACK HISTORY
            # =====================================

            CashbackTransaction.objects.create(

                customer_mobile=

                wallet.customer_mobile,

                order_id=

                order.id,

                cashback_amount=

                cashback,

                reward_points=

                reward_points
            )

            # =====================================
            # RESPONSE
            # =====================================

            return Response({

                "success": True,

                "message":

                "Payment Successful",

                "cashback":

                cashback,

                "reward_points":

                reward_points,

                "vip_level":

                wallet.vip_level
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })

            

class SingleOrderView(APIView):

    def get(self, request, id):

        order = Order.objects.get(id=id)

        serializer = OrderSerializer(order)

        return Response(serializer.data)
    
    
class UpdateDeliveryLocation(APIView):

    def post(self, request):

        order_id = request.data.get("order_id")

        latitude = request.data.get("latitude")

        longitude = request.data.get("longitude")

        order = Order.objects.get(id=order_id)

        location, created = DeliveryLocation.objects.get_or_create(
            order=order
        )

        location.latitude = latitude

        location.longitude = longitude

        location.save()

        return Response({

            "success": True
        })
        
        
        
class GetDeliveryLocation(APIView):

    def get(self, request, order_id):

        location = DeliveryLocation.objects.get(
            order_id=order_id
        )

        serializer = DeliveryLocationSerializer(location)

        return Response(serializer.data)
    
    
class DeliveryETAView(APIView):

    def get(self, request, id):

        try:

            order = Order.objects.get(id=id)

            # CUSTOMER LOCATION
            customer_lat = 23.0225
            customer_lng = 72.5714

            # DELIVERY BOY LOCATION
            rider_lat = order.delivery_latitude
            rider_lng = order.delivery_longitude

            # DISTANCE FORMULA
            distance = math.sqrt(

                (customer_lat - rider_lat) ** 2 +

                (customer_lng - rider_lng) ** 2

            )

            # AI TRAFFIC SYSTEM
            traffic_factor = random.randint(1, 5)

            # AI ETA CALCULATION
            eta = round(

                (distance * 120) + traffic_factor
            )

            if eta < 1:
                eta = 1

            return Response({

                "success": True,

                "eta": eta,
                
                "traffic": traffic_data,

                "traffic": traffic_factor,

                "distance": round(distance * 100, 2)

            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
        
class UpdateDeliveryLocationView(APIView):

    def post(self, request, id):

        try:

            order = Order.objects.get(id=id)

            order.delivery_latitude = request.data.get("latitude")

            order.delivery_longitude = request.data.get("longitude")

            order.save()
            
            channel_layer = get_channel_layer()

            async_to_sync(

                channel_layer.group_send

            )(

                f"order_{order.id}",

                {

                    "type":

                    "order_update",

                    "data": {

                        "delivery_latitude":

                        order.delivery_latitude,

                        "delivery_longitude":

                        order.delivery_longitude
                    }
                }
            )

            return Response({

                "success": True
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
            

class DeliveryBoySimulationView(APIView):

    def post(self, request, id):

        try:

            order = Order.objects.get(id=id)

            # MOVE RIDER TOWARD CUSTOMER

            customer_lat = 23.0225
            customer_lng = 72.5714

            current_lat = order.delivery_latitude
            current_lng = order.delivery_longitude

            # SMALL MOVEMENT
            current_lat -= 0.0005
            current_lng -= 0.0005

            # SAVE LOCATION
            order.delivery_latitude = current_lat
            order.delivery_longitude = current_lng

            order.save()

            # AUTO DELIVERED
            if abs(current_lat - customer_lat) < 0.001:

                order.status = "Delivered"
                

                fatigue_data = detect_rider_fatigue(

                    order.assigned_rider
                )

                order.save()

            return Response({

                "success": True,

                "latitude": current_lat,

                "longitude": current_lng,
                
                "fatigue": fatigue_data,

                "status": order.status
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
          
            
# =========================================
# UPDATE RIDER LIVE LOCATION
# =========================================

class UpdateRiderLocationView(APIView):

        def post(self, request):

            rider_id = request.data.get(
                "rider_id"
            )
            

            latitude = request.data.get(
                "latitude"
            )
            

            longitude = request.data.get(
                "longitude"
            )
            

            try:

                rider =  Rider.objects.get(
                    id=rider_id
                )
               

                rider.latitude = latitude
                rider.longitude = longitude

                rider.save()

                # =====================================
                # FIND ACTIVE ORDER
                # =====================================

                order =  Order.objects.filter(

                    rider=rider,
                    status="On The Way"

                ).first()
               

                if order:

                    # CUSTOMER LOCATION

                    customer_lat = float(order.latitude)
                    

                    customer_lng = float(order.longitude)

                    
                    # RIDER LOCATION

                    rider_lat = float(latitude)
                    

                    rider_lng = float(longitude)
                     
                    # DISTANCE

                    distance = calculate_distance(

                        rider_lat,
                        rider_lng,

                        customer_lat,
                        customer_lng
                    )
                    

                    # ETA

                    eta =  calculate_eta(distance)
                   

                    # SAVE

                    order.eta_minutes = eta

                    order.save()
                    
                    # =====================================
                    # WEBSOCKET LIVE UPDATE
                    # =====================================

                    channel_layer = get_channel_layer()

                    async_to_sync(

                        channel_layer.group_send

                    )(

                        f"order_{order.id}",

                        {

                            "type":

                            "order_update",

                            "data": {

                                "latitude":

                                rider_lat,

                                "longitude":

                                rider_lng,

                                "eta":

                                eta,

                                "status":

                                order.status
                            }
                        }
                    )

                return Response({

                    "success": True
                })

            except Exception as e:

                return Response({

                    "success": False,
                    "message": str(e)
                })
                

# =========================================
# CALCULATE DISTANCE
# =========================================

def calculate_distance(

    lat1,
    lon1,
    lat2,
    lon2
):

    return math.sqrt(

        (lat2 - lat1) ** 2 +

        (lon2 - lon1) ** 2
    )
    
    
# =========================================
# RIDER LOGIN API
# =========================================

class RiderLoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        try:

            email = request.data.get("email")
            password = request.data.get("password")

            rider = Rider.objects.filter(
                email=email
            ).first()

            # INVALID EMAIL

            if not rider:

                return Response({

                    "success": False,

                    "message":
                        "Invalid Email"

                }, status=400)

            # INVALID PASSWORD

            if rider.password != password:

                return Response({

                    "success": False,

                    "message":
                        "Invalid Password"

                }, status=400)

            # SUCCESS

            return Response({

                "success": True,

                "rider_id": rider.id,

                "name": rider.name,

                "email": rider.email,

                "message":
                    "Login Successful"

            })

        except Exception as e:

            return Response({

                "success": False,

                "message": str(e)

            }, status=500)



# =========================================
# RIDER DASHBOARD API
# =========================================

class RiderDashboardView(APIView):

    def get(self, request, rider_id):

        rider = Rider.objects.get(id=rider_id)

        serializer = RiderSerializer(rider)

        return Response({

            "success": True,

            "rider": serializer.data
        })


# =========================================
# RIDER ASSIGNED ORDERS
# =========================================

class RiderOrdersView(APIView):

    def get(self, request, rider_id):

        orders = Order.objects.filter(

            is_accepted=False,

            status="Preparing"

        ).order_by("-id")


        serializer = OrderSerializer(

                orders,

                many=True
            )

        return Response({

            "success": True,

            "orders": serializer.data
        })


# =========================================
# RIDER STATS API
# =========================================

class RiderStatsView(APIView):

    def get(self, request, rider_id):

        try:

            rider = Rider.objects.get(
                id=rider_id
            )

            orders = Order.objects.filter(
                assigned_rider=rider
            )

            completed_orders = orders.filter(
                status="Delivered"
            )

            earnings = 0

            for order in completed_orders:

                earnings += int(order.total_price) * 0.20

            return Response({

                "success": True,

                "total_orders":
                    orders.count(),

                "completed_orders":
                    completed_orders.count(),

                "earnings":
                    earnings,

                "available":
                    rider.is_available
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# UPDATE RIDER GPS
# =========================================

class UpdateRiderGPSAPIView(APIView): 
    
    
    def post(self, request, order_id): 
        
        try: 
            
            order = Order.objects.get( 
                id=order_id 
            ) 
            
            latitude = request.data.get( 
                "latitude" 
            ) 
            
            longitude = request.data.get( 
                "longitude" 
            ) 
            
            order.latitude = latitude 
            
            order.longitude = longitude 
            
            order.save() 
            
            return Response({ 
                "success": True, 
                "latitude": latitude, 
                "longitude": longitude 
            }) 
        
        except Exception as e: 
            
            return Response({ 
                "success": False, 
                "error": str(e) 
            })
            
            
# =========================================
# ACCEPT ORDER API
# =========================================

class AcceptOrderAPIView(APIView):

    def post(self, request, order_id):

        try:

            rider_id = request.data.get(
                    "rider_id"
                )

            order = Order.objects.get(
                id=order_id
            )

            rider = Rider.objects.get(
                id=rider_id
            )

            # ALREADY ASSIGNED

            if order.assigned_rider:

                return Response({

                    "success": False,

                    "message":
                        "Order Already Accepted"

                })

            # ASSIGN RIDER

            order.assigned_rider = rider

            order.status = "Out For Delivery"

            order.save()

            # BUSY

            rider.is_available = False

            rider.save()

            return Response({

                "success": True,

                "message":
                    "Order Accepted"
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# SEND CHAT MESSAGE
# =========================================

class SendChatMessageAPIView(APIView):

    def post(self, request):

        order_id = request.data.get("order_id")

        sender = request.data.get("sender")

        message = request.data.get("message")

        try:

            order = Order.objects.get(id=order_id)

            chat = ChatMessage.objects.create(

                order=order,

                sender=sender,

                message=message
            )

            return Response({

                "success": True,

                "message": "Message Sent"

            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# GET CHAT MESSAGES
# =========================================

class OrderChatAPIView(APIView):

    def get(self, request, order_id):

        messages = ChatMessage.objects.filter(

            order_id=order_id

        ).order_by("created_at")

        data = []

        for msg in messages:

            data.append({

                "sender": msg.sender,

                "message": msg.message,

                "created_at": msg.created_at
            })

        return Response(data)
    

# =========================================
# COMPLETE DELIVERY
# =========================================

class CompleteDeliveryAPIView(APIView):

    def post(self, request, order_id):

        try:

            order = Order.objects.get(
                id=order_id
            )

            rider = order.assigned_rider

            # DELIVERED

            order.status = "Delivered"
            
            send_push_notification(

                device.fcm_token,

                "Order Delivered",

                "Enjoy your meal 🍔"
            )

            order.save()

            # AVAILABLE AGAIN

            if rider:

                rider.is_available = True

                rider.save()

            return Response({

                "success": True,

                "message":
                    "Order Delivered"
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# CREATE ORDER
# =========================================

class CreateOrderView(APIView):

    def post(self, request):

        try:

            # =====================================
            # GET DATA
            # =====================================

            customer_name = request.data.get(
                "customer_name"
            )

            customer_mobile = request.data.get(
                "customer_mobile"
            )

            address = request.data.get(
                "address"
            )

            total_price = request.data.get(
                "total_price"
            )

            latitude = float(
                request.data.get("latitude")
            )

            longitude = float(
                request.data.get("longitude")
            )

            # =====================================
            # AI MULTI CITY RIDER SYSTEM
            # =====================================

            result = get_best_city_rider(

                latitude,
                longitude
            )

            best_rider = result.get("rider")

            city = result.get("city")

            # =====================================
            # AI LIVE TRAFFIC ETA
            # =====================================

            eta_data = calculate_ai_eta(

                best_rider.latitude,
                best_rider.longitude,

                latitude,
                longitude
            )

            eta = eta_data["eta_minutes"]

            # =====================================
            # CREATE ORDER
            # =====================================

            order = Order.objects.create(

                customer_name=customer_name,

                mobile=customer_mobile,

                address=address,

                total_price = float(total_price) + float( 
                    pricing["final_price"] 
                ),

                pricing = calculate_dynamic_price(

                    base_fee=30,

                    traffic=eta_data["traffic"],

                    weather=eta_data["weather"],

                    demand_level=random.randint(1, 10)
                ),
                
                base_delivery_fee=pricing["base_fee"],

                surge_multiplier=pricing["multiplier"],

                final_delivery_fee=pricing["final_price"],

                pricing_reason=", ".join(

                    pricing["reasons"]
                ),

                latitude=latitude,

                longitude=longitude,

                city=city,

                assigned_rider=best_rider,

                eta_minutes=eta,
                
                traffic_level=eta_data["traffic"]["traffic_level"],

                status="Preparing"
            )

            # =====================================
            # AI FRAUD DETECTION
            # =====================================

            try:

                fraud_result = detect_fraud(order)

                order.is_fraud = fraud_result.get(

                    "is_fraud",
                    False
                )

                order.fraud_score = fraud_result.get(

                    "fraud_score",
                    0
                )

                order.fraud_reason = ", ".join(

                    fraud_result.get(
                        "reasons",
                        []
                    )
                )

                order.save()
                
                from ai_engine.push_notification import (
                    send_push_notification
                )

                device = CustomerDevice.objects.filter(

                    customer_mobile=

                    customer_mobile

                ).first()

                if device:

                    send_push_notification(

                        device.fcm_token,

                        "Order Created",

                        f"Your Order #{order.id} was created."
                    )

            except Exception:

                pass

            # =====================================
            # UPDATE RIDER STATUS
            # =====================================

            if best_rider:

                best_rider.is_available = False

                best_rider.save()
                
                CustomerNotification.objects.create(

                    customer_mobile=

                    customer_mobile,

                    title="Order Created",

                    message=

                    f"Order #{order.id} created successfully."
                )

            return Response({

                "success": True,

                "message":
                "Order Created Successfully",

                "order_id": order.id,

                "city": city,

                "eta": eta,
                
                "dynamic_pricing": {

                    "base_fee":

                    pricing["base_fee"],

                    "multiplier":

                    pricing["multiplier"],

                    "final_fee":

                    pricing["final_price"],

                    "reasons":

                    pricing["reasons"]
                },

                
                "traffic": eta_data["traffic"],

                "rider": {

                    "id":
                    best_rider.id
                    if best_rider else None,

                    "name":
                    best_rider.name
                    if best_rider else None,

                    "mobile":
                    best_rider.mobile
                    if best_rider else None

                }

            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)

            })



# =========================================
# ALL ORDERS
# =========================================

class AllOrdersView(APIView):

    def get(self, request):

        orders = Order.objects.all().order_by(
            "-id"
        )

        serializer = OrderSerializer(

            orders,

            many=True
        )

        return Response(
            serializer.data
        )



class ClusterOrdersView(APIView):

    def get(self, request):

        pending_orders = Order.objects.filter(

            status="Pending",
            is_accepted=False
        )

        cluster_orders = find_cluster_orders(
            pending_orders
        )

        data = []

        for order in cluster_orders:

            data.append({

                "id": order.id,
                "customer_name": order.customer_name,
                "latitude": order.delivery_latitude,
                "longitude": order.delivery_longitude,
                "total_price": str(order.total_price)
            })

        return Response({

            "success": True,
            "cluster_orders": data
        })
        
        
        
# =========================================
# AI SMART PRIORITY VIEW
# =========================================

class SmartPriorityView(APIView):

    def get(self, request):

        orders = Order.objects.filter(

            status="Pending",
            is_accepted=False
        )

        final_data = []

        for order in orders:

            priority = calculate_priority(order)

            final_data.append({

                "id": order.id,

                "customer_name":
                order.customer_name,

                "total_price":
                str(order.total_price),

                "priority_score":
                priority["score"],

                "distance":
                priority["distance"],

                "created_at":
                order.created_at
            })

        # =================================
        # SORT BY PRIORITY
        # =================================

        final_data = sorted(

            final_data,

            key=lambda x:
            x["priority_score"],

            reverse=True
        )

        return Response({

            "success": True,

            "orders": final_data
        })
        
        

# =========================================
# AI AUTO RIDER ASSIGN VIEW
# =========================================

class AutoAssignRiderView(APIView):

    def post(self, request, id):

        try:

            order = Order.objects.get(id=id)

            result = auto_assign_rider(order)

            return Response(result)

        except Exception as e:

            return Response({

                "success": False,

                "message": str(e)
            })
            
            

# =========================================
# AI DELIVERY HEATMAP VIEW
# =========================================

class DeliveryHeatmapView(APIView):

    def get(self, request):

        orders = Order.objects.filter(

            status__in=[

                "Pending",
                "Preparing",
                "Out For Delivery",
                "Delivered"
            ]
        )

        heatmap_data = generate_heatmap(
            orders
        )

        return Response({

            "success": True,

            "heatmap":
            heatmap_data
        })
        
        
# =========================================
# AI ORDER BATCH VIEW
# =========================================

class OrderBatchView(APIView):

    def get(self, request):

        batches = create_order_batches()

        return Response({

            "success": True,

            "batches": batches
        })
        
        

# =========================================
# AI DEMAND PREDICTION VIEW
# =========================================

class PredictiveDemandView(APIView):

    def get(self, request):

        data = predict_delivery_demand()

        return Response({

            "success": True,

            "prediction": data
        })
        
        
        
# =========================================
# RIDER PERFORMANCE ANALYTICS VIEW
# =========================================

class RiderAnalyticsView(APIView):

    def get(self, request):

        data = rider_performance_analytics()

        return Response({

            "success": True,

            "analytics": data
        })
        
        

# =========================================
# FRAUD ORDERS VIEW
# =========================================

class FraudOrdersView(APIView):

    def get(self, request):

        fraud_orders = Order.objects.filter(

            is_fraud=True
        ).order_by("-created_at")

        data = []

        for order in fraud_orders:

            data.append({

                "id": order.id,

                "customer_name": order.customer_name,

                "mobile": order.mobile,

                "amount": str(order.total_price),

                "fraud_score": order.fraud_score,

                "fraud_reason": order.fraud_reason,

                "status": order.status
            })

        return Response({

            "success": True,

            "fraud_orders": data
        })
        
        

# =========================================
# CREATE WITHDRAW REQUEST
# =========================================

class CreateWithdrawView(APIView):

    def post(self, request):

        try:

            rider_id = request.data.get(
                "rider_id"
            )

            amount = float(

                request.data.get(
                    "amount"
                )
            )

            payment_method = request.data.get(
                "payment_method"
            )

            rider = Rider.objects.get(
                id=rider_id
            )

            wallet = RiderWallet.objects.get(
                rider=rider
            )

            # =====================================
            # AI CHECK
            # =====================================

            ai_result = withdraw_ai_check(

                wallet.available_balance,
                amount
            )

            if not ai_result["allowed"]:

                return Response({

                    "success": False,

                    "message":
                    ai_result["reason"]
                })

            # =====================================
            # CREATE WITHDRAW
            # =====================================

            withdraw = RiderWithdraw.objects.create(

                rider=rider,

                amount=amount,

                payment_method=payment_method,

                upi_id=request.data.get(
                    "upi_id"
                ),

                bank_name=request.data.get(
                    "bank_name"
                ),

                account_number=request.data.get(
                    "account_number"
                ),

                ifsc_code=request.data.get(
                    "ifsc_code"
                )
            )

            # =====================================
            # HOLD BALANCE
            # =====================================

            wallet.available_balance -= amount

            wallet.save()

            return Response({

                "success": True,

                "message":
                "Withdraw Request Submitted",

                "withdraw_id":
                withdraw.id
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# RIDER LEADERBOARD API
# =========================================

class RiderLeaderboardView(APIView):

    def get(self, request):

        riders = RiderPerformance.objects.all().order_by(

            "-performance_score"
        )[:10]

        data = []

        rank = 1

        for rider in riders:

            data.append({

                "position": rank,

                "rider_name": rider.rider.name,

                "score": rider.performance_score,

                "rank": rider.rider_rank,

                "deliveries":
                rider.successful_deliveries
            })

            rank += 1

        return Response({

            "success": True,

            "leaderboard": data
        })


# =========================================
# RIDER ACHIEVEMENT API
# =========================================

class RiderAchievementView(APIView):

    def get(self, request, rider_id):

        achievements = RiderAchievement.objects.filter(

            rider_id=rider_id
        ).order_by("-unlocked_at")

        data = []

        for item in achievements:

            data.append({

                "badge_name": item.badge_name,

                "badge_icon": item.badge_icon,

                "description": item.description,

                "xp_reward": item.xp_reward,

                "unlocked_at": item.unlocked_at
            })

        return Response({

            "success": True,

            "achievements": data
        })


# =========================================
# RIDER MISSIONS API
# =========================================

class RiderMissionView(APIView):

    def get(self, request, rider_id):

        missions = RiderMission.objects.filter(

            rider_id=rider_id
        ).order_by("-created_at")

        data = []

        for mission in missions:

            data.append({

                "title": mission.mission_title,

                "description":
                mission.mission_description,

                "target":
                mission.target_count,

                "completed":
                mission.completed_count,

                "reward":
                mission.reward_amount,

                "xp":
                mission.xp_reward,

                "is_completed":
                mission.is_completed
            })

        return Response({

            "success": True,

            "missions": data
        })


# =========================================
# RIDER STREAK API
# =========================================

class RiderStreakView(APIView):

    def get(self, request, rider_id):

        try:

            streak = RiderStreak.objects.get(

                rider_id=rider_id
            )

            return Response({

                "success": True,

                "current_streak":
                streak.current_streak,

                "highest_streak":
                streak.highest_streak,

                "xp":
                streak.total_xp,

                "level":
                streak.rider_level,

                "multiplier":
                streak.streak_multiplier
            })

        except:

            return Response({

                "success": False,

                "message":
                "No streak found"
            })



# =========================================
# RIDER DISCIPLINE API
# =========================================

class RiderDisciplineView(APIView):

    def get(self, request, rider_id):

        try:

            discipline = RiderDiscipline.objects.get(

                rider_id=rider_id
            )

            return Response({

                "success": True,

                "trust_score":
                discipline.trust_score,

                "warnings":
                discipline.warning_count,

                "late_deliveries":
                discipline.late_delivery_count,

                "fraud_count":
                discipline.fraud_count,

                "reputation":
                discipline.reputation_level,

                "is_suspended":
                discipline.is_suspended,

                "reason":
                discipline.suspension_reason
            })

        except:

            return Response({

                "success": False,

                "message":
                "Discipline data not found"
            })



# =========================================
# RIDER CLOCK IN
# =========================================

class RiderClockInView(APIView):

    def post(self, request, rider_id):

        try:

            rider = Rider.objects.get(

                id=rider_id
            )

            shift = rider_clock_in(rider)

            return Response({

                "success": True,

                "message":
                "Clock In Successful",

                "clock_in":
                shift.clock_in
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# RIDER CLOCK OUT
# =========================================

class RiderClockOutView(APIView):

    def post(self, request, rider_id):

        try:

            rider = Rider.objects.get(

                id=rider_id
            )

            result = rider_clock_out(rider)

            if not result:

                return Response({

                    "success": False,

                    "message":
                    "No Active Shift"
                })

            return Response({

                "success": True,

                "message":
                "Clock Out Successful",

                "data": result
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# RIDER SHIFT ANALYTICS
# =========================================

class RiderShiftAnalyticsView(APIView):

    def get(self, request, rider_id):

        shifts = RiderShift.objects.filter(

            rider_id=rider_id
        ).order_by("-created_at")

        total_hours = sum(

            shift.total_hours

            for shift in shifts
        )

        total_bonus = sum(

            shift.peak_hour_bonus

            for shift in shifts
        )

        avg_productivity = 0

        if shifts.count() > 0:

            avg_productivity = sum(

                shift.productivity_score

                for shift in shifts

            ) / shifts.count()

        return Response({

            "success": True,

            "total_shifts":
            shifts.count(),

            "total_hours":
            total_hours,

            "total_bonus":
            total_bonus,

            "avg_productivity":
            round(avg_productivity, 2)
        })


# =========================================
# GENERATE AI SCHEDULE
# =========================================

class GenerateRiderScheduleView(APIView):

    def post(self, request, rider_id):

        try:

            rider = Rider.objects.get(

                id=rider_id
            )

            result = generate_rider_schedule(

                rider
            )

            return Response({

                "success": True,

                "message":
                "AI Schedule Generated",

                "data": result
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# GET BEST AI RIDER
# =========================================

class BestScheduledRiderView(APIView):

    def get(self, request):

        rider = get_best_scheduled_rider()

        if not rider:

            return Response({

                "success": False,

                "message":
                "No Rider Available"
            })

        return Response({

            "success": True,

            "rider": {

                "id": rider.id,

                "name": rider.name,

                "mobile": rider.mobile
            }
        })


# =========================================
# RIDER MOOD ANALYTICS
# =========================================

class RiderMoodAPIView(APIView):

    def get(self, request, rider_id):

        try:

            rider = Rider.objects.get(
                id=rider_id
            )

            ai_data = detect_rider_mood(
                rider
            )

            # SAVE AI DATA

            rider.stress_level = ai_data[
                "stress_level"
            ]

            rider.mood_status = ai_data[
                "mood"
            ]

            rider.mental_health_score = ai_data[
                "mental_health"
            ]

            rider.save()

            return Response({

                "success": True,

                "rider": rider.name,

                "stress_level":
                rider.stress_level,

                "mood_status":
                rider.mood_status,

                "mental_health_score":
                rider.mental_health_score,

                "reasons":
                ai_data["reasons"]
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
            

# =========================================
# RIDER SAFETY API
# =========================================

class RiderSafetyAPIView(APIView):

    def post(self, request):

        try:

            rider_id = request.data.get(
                "rider_id"
            )

            speed = float(

                request.data.get(
                    "speed",
                    0
                )
            )

            sudden_brakes = int(

                request.data.get(
                    "sudden_brakes",
                    0
                )
            )

            rider = Rider.objects.get(
                id=rider_id
            )

            ai_result = detect_rider_safety(

                speed,
                sudden_brakes,
                rider.overspeed_count
            )

            # =================================
            # SAVE AI DATA
            # =================================

            rider.safety_score = ai_result[
                "safety_score"
            ]

            rider.last_speed = speed

            rider.sudden_brake_count = sudden_brakes

            # =================================
            # OVER SPEED TRACKING
            # =================================

            if speed > 80:

                rider.overspeed_count += 1

            # =================================
            # ACCIDENT MODE
            # =================================

            if ai_result["danger"]:

                rider.is_in_accident = True

                rider.emergency_mode = True

            rider.save()

            return Response({

                "success": True,

                "rider": rider.name,

                "speed": speed,

                "safety_score":
                rider.safety_score,

                "danger":
                rider.is_in_accident,

                "reasons":
                ai_result["reasons"]
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
            

# =========================================
# CREATE SOS ALERT
# =========================================

class CreateSOSView(APIView):

    def post(self, request):

        try:

            rider_id = request.data.get(
                "rider_id"
            )

            order_id = request.data.get(
                "order_id"
            )

            latitude = request.data.get(
                "latitude"
            )

            longitude = request.data.get(
                "longitude"
            )

            emergency_type = request.data.get(
                "emergency_type"
            )

            message = request.data.get(
                "message"
            )

            rider = Rider.objects.get(
                id=rider_id
            )

            order = None

            if order_id:

                order = Order.objects.get(
                    id=order_id
                )

            sos = RiderSOS.objects.create(

                rider=rider,

                order=order,

                latitude=latitude,

                longitude=longitude,

                emergency_type=emergency_type,

                message=message
            )

            return Response({

                "success": True,

                "message":
                "SOS Alert Sent",

                "sos_id": sos.id
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
            

# =========================================
# RESOLVE SOS
# =========================================

class ResolveSOSView(APIView):

    def post(self, request, id):

        try:

            sos = RiderSOS.objects.get(
                id=id
            )

            sos.is_resolved = True

            sos.save()

            return Response({

                "success": True,

                "message":
                "SOS Resolved"
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            


class VoiceSOSView(APIView):

    def post(self, request):

        try:

            latitude = request.data.get("latitude")
            longitude = request.data.get("longitude")
            message = request.data.get("message", "")
            emergency_type = request.data.get("emergency_type", "Voice SOS")

            # =========================
            # FIND NEAREST AVAILABLE RIDER
            # =========================

            rider = Rider.objects.filter(
                is_available=True
            ).first()

            # =========================
            # CREATE SOS RECORD
            # =========================

            sos = RiderSOS.objects.create(

                rider=rider,
                order=None,

                latitude=latitude,
                longitude=longitude,

                emergency_type=emergency_type,
                message=message
            )

            # =========================
            # RESPONSE
            # =========================

            return Response({

                "success": True,
                "message": "🚨 Voice SOS Triggered Successfully",
                "sos_id": sos.id,

                "rider": {
                    "id": rider.id if rider else None,
                    "name": rider.name if rider else None
                }

            })

        except Exception as e:

            return Response({

                "success": False,
                "error": str(e)

            })
            
            
            
# =========================================
# LIVE HEATMAP API
# =========================================

class DeliveryHeatmapView(APIView):

    def get(self, request):

        heatmap_data = []

        # =====================================
        # ORDERS
        # =====================================

        orders = Order.objects.exclude(
            latitude__isnull=True,
            longitude__isnull=True
        )

        for order in orders:

            heatmap_data.append({

                "lat": order.latitude,
                "lng": order.longitude,
                "weight": 1,
                "type": "order"
            })

        # =====================================
        # RIDERS
        # =====================================

        riders = Rider.objects.exclude(
            latitude__isnull=True,
            longitude__isnull=True
        )

        for rider in riders:

            heatmap_data.append({

                "lat": rider.latitude,
                "lng": rider.longitude,
                "weight": 0.5,
                "type": "rider"
            })

        return Response({

            "success": True,
            "data": heatmap_data
        })
        
        
# =========================================
# RESTAURANT REGISTER
# =========================================

class RestaurantRegisterView(APIView):

    def post(self, request):

        try:

            restaurant = Restaurant.objects.create(

                name=request.data.get("name"),

                owner_name=request.data.get(
                    "owner_name"
                ),

                email=request.data.get("email"),

                mobile=request.data.get("mobile"),

                password=request.data.get(
                    "password"
                ),

                address=request.data.get(
                    "address"
                ),

                city=request.data.get(
                    "city"
                ),

                latitude=request.data.get(
                    "latitude"
                ),

                longitude=request.data.get(
                    "longitude"
                )
            )

            return Response({

                "success": True,

                "message":
                "Restaurant Registered",

                "restaurant_id":
                restaurant.id
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# RESTAURANT LOGIN
# =========================================

class RestaurantLoginView(APIView):

    def post(self, request):

        try:

            email = request.data.get("email")

            password = request.data.get("password")

            # =========================
            # FIND OWNER
            # =========================

            owner = RestaurantOwner.objects.filter(

                email=email

            ).first()

            if not owner:

                return Response({

                    "success": False,

                    "message":
                    "Restaurant not found"
                })

            # =========================
            # PASSWORD CHECK
            # =========================

            if owner.password != password:

                return Response({

                    "success": False,

                    "message":
                    "Invalid password"
                })

            # =========================
            # JWT TOKEN
            # =========================

            refresh = RefreshToken.for_user(owner)

            # =========================
            # RESPONSE
            # =========================

            return Response({

                "success": True,

                "message":
                "Login Successful",

                "token": str(refresh.access_token),

                "refresh": str(refresh),

                "restaurant_owner": {

                    "id": owner.id,

                    "name": owner.name,

                    "email": owner.email,

                    "restaurant":

                    owner.restaurant.name
                }
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# RESTAURANT DASHBOARD API
# =========================================

class RestaurantDashboardView(APIView):

    def get(self, request, restaurant_id):

        try:

            # =====================================
            # GET RESTAURANT
            # =====================================

            restaurant = Restaurant.objects.get(

                id=restaurant_id
            )

            # =====================================
            # GET ORDERS
            # =====================================

            orders = Order.objects.filter(

                restaurant=restaurant
            )

            # =====================================
            # TOTAL ORDERS
            # =====================================

            total_orders = orders.count()

            # =====================================
            # PENDING ORDERS
            # =====================================

            pending_orders = orders.filter(

                status="Preparing"
            ).count()

            # =====================================
            # DELIVERED ORDERS
            # =====================================

            delivered_orders = orders.filter(

                status="Delivered"
            ).count()

            # =====================================
            # CANCELLED ORDERS
            # =====================================

            cancelled_orders = orders.filter(

                status="Cancelled"
            ).count()

            # =====================================
            # LIVE ORDERS
            # =====================================

            live_orders = orders.filter(

                status__in=[

                    "Preparing",
                    "Picked",
                    "On The Way"
                ]
            ).count()

            # =====================================
            # TOTAL REVENUE
            # =====================================

            total_revenue = orders.filter(

                status="Delivered"

            ).aggregate(

                total=Sum("total_price")

            )["total"] or 0

            # =====================================
            # TODAY REVENUE
            # =====================================

            today = now().date()

            today_revenue = orders.filter(

                created_at__date=today,

                status="Delivered"

            ).aggregate(

                total=Sum("total_price")

            )["total"] or 0

            # =====================================
            # WEEK REVENUE
            # =====================================

            week_ago = today - timedelta(days=7)

            weekly_revenue = orders.filter(

                created_at__date__gte=week_ago,

                status="Delivered"

            ).aggregate(

                total=Sum("total_price")

            )["total"] or 0

            # =====================================
            # MONTH REVENUE
            # =====================================

            month_ago = today - timedelta(days=30)

            monthly_revenue = orders.filter(

                created_at__date__gte=month_ago,

                status="Delivered"

            ).aggregate(

                total=Sum("total_price")

            )["total"] or 0

            # =====================================
            # POPULAR FOODS
            # =====================================

            popular_foods = Food.objects.filter(

                restaurant=restaurant

            ).annotate(

                total_orders=Count("id")

            ).order_by(

                "-total_orders"

            )[:5]

            # =====================================
            # FOOD LIST
            # =====================================

            popular_food_data = []

            for food in popular_foods:

                popular_food_data.append({

                    "id": food.id,

                    "name": food.name,

                    "price": food.price,

                    "image": food.image.url if food.image else None,

                    "orders": food.total_orders
                })

            # =====================================
            # RESPONSE
            # =====================================

            return Response({

                "success": True,

                "restaurant": {

                    "id": restaurant.id,

                    "name": restaurant.name,

                    "city": restaurant.city,

                    "address": restaurant.address
                },

                "analytics": {

                    "total_orders":
                    total_orders,

                    "pending_orders":
                    pending_orders,

                    "delivered_orders":
                    delivered_orders,

                    "cancelled_orders":
                    cancelled_orders,

                    "live_orders":
                    live_orders,

                    "total_revenue":
                    total_revenue,

                    "today_revenue":
                    today_revenue,

                    "weekly_revenue":
                    weekly_revenue,

                    "monthly_revenue":
                    monthly_revenue
                },

                "popular_foods":
                popular_food_data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# ADD FOOD API
# =========================================

class AddFoodView(APIView):

    parser_classes = [

        MultiPartParser,
        FormParser
    ]

    def post(self, request):

        try:

            restaurant_id = request.data.get(
                "restaurant_id"
            )

            restaurant = Restaurant.objects.get(
                id=restaurant_id
            )

            food = Food.objects.create(

                restaurant=restaurant,

                name=request.data.get("name"),

                description=request.data.get(
                    "description"
                ),

                price=request.data.get("price"),

                category=request.data.get(
                    "category"
                ),

                image=request.FILES.get(
                    "image"
                ),

                is_available=True
            )

            return Response({

                "success": True,

                "message":
                "Food Added Successfully",

                "food": FoodSerializer(food).data
            })

        except Exception as e:

            return Response({

                "success": False,
                "error": str(e)
            })


# =========================================
# RESTAURANT FOOD LIST
# =========================================

class RestaurantFoodListView(APIView):

    def get(self, request, restaurant_id):

        foods = Food.objects.filter(

            restaurant_id=restaurant_id

        ).order_by("-id")

        serializer = FoodSerializer(

            foods,
            many=True
        )

        return Response({

            "success": True,

            "foods": serializer.data
        })



# =========================================
# UPDATE FOOD
# =========================================

class UpdateFoodView(APIView):

    parser_classes = [

        MultiPartParser,
        FormParser
    ]

    def put(self, request, food_id):

        try:

            food = Food.objects.get(id=food_id)

            food.name = request.data.get(
                "name",
                food.name
            )

            food.description = request.data.get(
                "description",
                food.description
            )

            food.price = request.data.get(
                "price",
                food.price
            )

            food.category = request.data.get(
                "category",
                food.category
            )

            if request.FILES.get("image"):

                food.image = request.FILES.get(
                    "image"
                )

            food.save()

            return Response({

                "success": True,

                "message":
                "Food Updated Successfully",

                "food":
                FoodSerializer(food).data
            })

        except Exception as e:

            return Response({

                "success": False,
                "error": str(e)
            })


# =========================================
# DELETE FOOD
# =========================================

class DeleteFoodView(APIView):

    def delete(self, request, food_id):

        try:

            food = Food.objects.get(id=food_id)

            food.delete()

            return Response({

                "success": True,

                "message":
                "Food Deleted Successfully"
            })

        except Exception as e:

            return Response({

                "success": False,
                "error": str(e)
            })



# =========================================
# CREATE CUSTOMER WALLET
# =========================================

class CreateWalletView(APIView):

    def post(self, request):

        try:

            customer_name = request.data.get(
                "customer_name"
            )

            customer_mobile = request.data.get(
                "customer_mobile"
            )

            wallet, created = CustomerWallet.objects.get_or_create(

                customer_mobile=customer_mobile,

                defaults={

                    "customer_name": customer_name
                }
            )

            serializer = CustomerWalletSerializer(wallet)

            return Response({

                "success": True,
                "wallet": serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,
                "error": str(e)
            })


# =========================================
# ADD MONEY TO WALLET
# =========================================

class AddMoneyView(APIView):

    def post(self, request):

        try:

            customer_mobile = request.data.get(
                "customer_mobile"
            )

            amount = float(

                request.data.get("amount")
            )

            wallet = CustomerWallet.objects.get(

                customer_mobile=customer_mobile
            )

            wallet.balance += amount

            wallet.save()

            WalletTransaction.objects.create(

                wallet=wallet,

                amount=amount,

                transaction_type="credit",

                description="Money Added"
            )

            return Response({

                "success": True,

                "balance": wallet.balance
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# WALLET BALANCE
# =========================================

class WalletBalanceView(APIView):

    def get(self, request, mobile):

        try:

            wallet = CustomerWallet.objects.get(

                customer_mobile=mobile
            )

            serializer = CustomerWalletSerializer(wallet)

            return Response({

                "success": True,

                "wallet": serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# WALLET HISTORY
# =========================================

class WalletHistoryView(APIView):

    def get(self, request, mobile):

        try:

            wallet = CustomerWallet.objects.get(

                customer_mobile=mobile
            )

            transactions = WalletTransaction.objects.filter(

                wallet=wallet
            ).order_by("-created_at")

            serializer = WalletTransactionSerializer(

                transactions,
                many=True
            )

            return Response({

                "success": True,

                "transactions": serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# WALLET PAYMENT SYSTEM
# =========================================

class WalletPaymentView(APIView):

    def post(self, request):

        try:

            order_id = request.data.get(
                "order_id"
            )

            customer_mobile = request.data.get(
                "customer_mobile"
            )

            # =====================================
            # GET ORDER
            # =====================================

            order = Order.objects.get(
                id=order_id
            )

            # =====================================
            # GET WALLET
            # =====================================

            wallet = CustomerWallet.objects.get(

                customer_mobile=customer_mobile
            )

            total_amount = float(
                order.total_price
            )

            # =====================================
            # CHECK BALANCE
            # =====================================

            if wallet.balance < total_amount:

                return Response({

                    "success": False,

                    "message":

                    "Insufficient Wallet Balance"
                })

            # =====================================
            # DEDUCT MONEY
            # =====================================

            wallet.balance -= total_amount

            wallet.save()

            # =====================================
            # UPDATE ORDER
            # =====================================

            order.payment_method = "Wallet"

            order.payment_status = "Paid"

            order.wallet_paid_amount = total_amount

            # =====================================
            # CASHBACK
            # =====================================

            cashback = round(

                total_amount * 0.05,
                2
            )

            order.cashback_amount = cashback

            order.save()

            # =====================================
            # ADD CASHBACK
            # =====================================

            wallet.balance += cashback

            wallet.save()

            # =====================================
            # TRANSACTION
            # =====================================

            WalletTransaction.objects.create(

                wallet=wallet,

                amount=total_amount,

                transaction_type="debit",

                description=

                f"Wallet Payment For Order #{order.id}"
            )

            WalletTransaction.objects.create(

                wallet=wallet,

                amount=cashback,

                transaction_type="cashback",

                description=

                f"Cashback For Order #{order.id}"
            )

            # =====================================
            # RESPONSE
            # =====================================

            return Response({

                "success": True,

                "message":

                "Wallet Payment Successful",

                "wallet_balance":

                wallet.balance,

                "cashback":

                cashback,

                "order_id":

                order.id
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# WALLET REFUND SYSTEM
# =========================================

class WalletRefundView(APIView):

    def post(self, request):

        try:

            order_id = request.data.get(
                "order_id"
            )

            order = Order.objects.get(
                id=order_id
            )

            wallet = CustomerWallet.objects.get(

                customer_mobile=
                order.mobile
            )

            refund_amount = float(
                order.wallet_paid_amount
            )

            # =====================================
            # REFUND
            # =====================================

            wallet.balance += refund_amount

            wallet.save()

            # =====================================
            # TRANSACTION
            # =====================================

            WalletTransaction.objects.create(

                wallet=wallet,

                amount=refund_amount,

                transaction_type="refund",

                description=

                f"Refund For Order #{order.id}"
            )

            # =====================================
            # UPDATE ORDER
            # =====================================

            order.payment_status = "Refunded"

            order.save()

            return Response({

                "success": True,

                "refund_amount":

                refund_amount,

                "wallet_balance":

                wallet.balance
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# CREATE RAZORPAY ORDER
# =========================================

class CreateRazorpayOrderView(APIView):

    def post(self, request):

        try:

            order_id = request.data.get(
                "order_id"
            )

            order = Order.objects.get(
                id=order_id
            )

            amount = int(

                float(order.total_price) * 100
            )

            # =====================================
            # CREATE RAZORPAY ORDER
            # =====================================

            payment = razorpay_client.order.create({

                "amount": amount,

                "currency": "INR",

                "payment_capture": 1
            })

            return Response({

                "success": True,

                "razorpay_order_id":

                payment["id"],

                "amount": amount,

                "key":

                settings.RAZORPAY_KEY_ID
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# VERIFY RAZORPAY PAYMENT
# =========================================

class VerifyRazorpayPaymentView(APIView):

    def post(self, request):

        try:

            order_id = request.data.get(
                "order_id"
            )

            payment_id = request.data.get(
                "payment_id"
            )

            razorpay_order_id = request.data.get(
                "razorpay_order_id"
            )

            signature = request.data.get(
                "signature"
            )

            # =====================================
            # VERIFY SIGNATURE
            # =====================================

            razorpay_client.utility.verify_payment_signature({

                'razorpay_order_id':
                razorpay_order_id,

                'razorpay_payment_id':
                payment_id,

                'razorpay_signature':
                signature
            })

            # =====================================
            # UPDATE ORDER
            # =====================================

            order = Order.objects.get(
                id=order_id
            )

            order.payment_status = "Paid"

            order.payment_method = "Razorpay"

            order.save()

            return Response({

                "success": True,

                "message":

                "Payment Successful"
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# STRIPE PAYMENT INTENT
# =========================================

class CreateStripePaymentView(APIView):

    def post(self, request):

        try:

            order_id = request.data.get(
                "order_id"
            )

            order = Order.objects.get(
                id=order_id
            )

            amount = int(

                float(order.total_price) * 100
            )

            # =====================================
            # CREATE STRIPE INTENT
            # =====================================

            intent = stripe.PaymentIntent.create(

                amount=amount,

                currency='inr'
            )

            return Response({

                "success": True,

                "client_secret":

                intent.client_secret
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# CREATE MEMBERSHIP PLAN
# =========================================

class CreateMembershipPlanView(APIView):

    def post(self, request):

        try:

            serializer = MembershipPlanSerializer(

                data=request.data
            )

            if serializer.is_valid():

                serializer.save()

                return Response({

                    "success": True,

                    "plan": serializer.data
                })

            return Response({

                "success": False,

                "errors": serializer.errors
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# PURCHASE MEMBERSHIP
# =========================================

class PurchaseMembershipView(APIView):

    def post(self, request):

        try:

            customer_name = request.data.get(
                "customer_name"
            )

            customer_mobile = request.data.get(
                "customer_mobile"
            )

            plan_id = request.data.get(
                "plan_id"
            )

            plan = MembershipPlan.objects.get(
                id=plan_id
            )

            expiry = timezone.now() + timedelta(

                days=plan.duration_days
            )

            membership = CustomerMembership.objects.create(

                customer_name=customer_name,

                customer_mobile=customer_mobile,

                plan=plan,

                expiry_date=expiry
            )

            serializer = CustomerMembershipSerializer(

                membership
            )

            return Response({

                "success": True,

                "membership": serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# CHECK MEMBERSHIP
# =========================================

class CheckMembershipView(APIView):

    def get(self, request, mobile):

        try:

            membership = CustomerMembership.objects.filter(

                customer_mobile=mobile,

                is_active=True,

                expiry_date__gte=timezone.now()

            ).first()

            if not membership:

                return Response({

                    "success": False,

                    "message":

                    "No Active Membership"
                })

            serializer = CustomerMembershipSerializer(

                membership
            )

            return Response({

                "success": True,

                "membership": serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# CREATE COUPON
# =========================================

class CreateCouponView(APIView):

    def post(self, request):

        try:

            serializer = CouponSerializer(

                data=request.data
            )

            if serializer.is_valid():

                serializer.save()

                return Response({

                    "success": True,

                    "coupon": serializer.data
                })

            return Response({

                "success": False,

                "errors": serializer.errors
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# APPLY COUPON
# =========================================

class ApplyCouponView(APIView):

    def post(self, request):

        try:

            coupon_code = request.data.get(
                "coupon_code"
            )

            order_amount = float(

                request.data.get(
                    "order_amount"
                )
            )

            coupon = Coupon.objects.get(

                code=coupon_code,

                is_active=True
            )

            # =====================================
            # EXPIRY CHECK
            # =====================================

            if coupon.expiry_date < timezone.now():

                return Response({

                    "success": False,

                    "message":

                    "Coupon Expired"
                })

            # =====================================
            # USAGE CHECK
            # =====================================

            if coupon.used_count >= coupon.usage_limit:

                return Response({

                    "success": False,

                    "message":

                    "Coupon Usage Limit Exceeded"
                })

            # =====================================
            # MINIMUM AMOUNT
            # =====================================

            if order_amount < float(

                coupon.minimum_order_amount
            ):

                return Response({

                    "success": False,

                    "message":

                    f"Minimum Order ₹{coupon.minimum_order_amount}"
                })

            # =====================================
            # DISCOUNT CALCULATION
            # =====================================

            discount = 0

            if coupon.coupon_type == "percentage":

                discount = (

                    order_amount *

                    float(coupon.discount_value)
                ) / 100

                if coupon.maximum_discount > 0:

                    discount = min(

                        discount,

                        float(coupon.maximum_discount)
                    )

            else:

                discount = float(

                    coupon.discount_value
                )

            final_amount = order_amount - discount

            return Response({

                "success": True,

                "coupon": coupon.code,

                "discount": round(discount, 2),

                "final_amount": round(final_amount, 2)
            })

        except Coupon.DoesNotExist:

            return Response({

                "success": False,

                "message":

                "Invalid Coupon"
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# APPLY REFERRAL CODE
# =========================================

class ApplyReferralCodeView(APIView):

    def post(self, request):

        try:

            customer_mobile = request.data.get(
                "customer_mobile"
            )

            referral_code = request.data.get(
                "referral_code"
            )

            # =====================================
            # FIND INVITER
            # =====================================

            inviter_wallet = CustomerWallet.objects.get(

                referral_code=referral_code
            )

            customer_wallet = CustomerWallet.objects.get(

                customer_mobile=customer_mobile
            )

            # =====================================
            # PREVENT SELF REFERRAL
            # =====================================

            if inviter_wallet.customer_mobile == customer_mobile:

                return Response({

                    "success": False,

                    "message":

                    "Cannot Refer Yourself"
                })

            # =====================================
            # PREVENT MULTIPLE REFERRALS
            # =====================================

            if customer_wallet.referred_by:

                return Response({

                    "success": False,

                    "message":

                    "Referral Already Applied"
                })

            # =====================================
            # BONUS SYSTEM
            # =====================================

            inviter_bonus = 100
            invited_bonus = 50

            # =====================================
            # UPDATE INVITER WALLET
            # =====================================

            inviter_wallet.balance += inviter_bonus

            inviter_wallet.total_referral_earnings += inviter_bonus

            inviter_wallet.save()

            # =====================================
            # UPDATE INVITED USER
            # =====================================

            customer_wallet.balance += invited_bonus

            customer_wallet.referred_by = referral_code

            customer_wallet.save()

            # =====================================
            # SAVE REFERRAL HISTORY
            # =====================================

            ReferralTransaction.objects.create(

                inviter_mobile=

                inviter_wallet.customer_mobile,

                invited_mobile=

                customer_mobile,

                referral_code=

                referral_code,

                bonus_amount=

                inviter_bonus
            )

            return Response({

                "success": True,

                "message":

                "Referral Applied Successfully",

                "inviter_bonus":

                inviter_bonus,

                "your_bonus":

                invited_bonus
            })

        except CustomerWallet.DoesNotExist:

            return Response({

                "success": False,

                "message":

                "Invalid Referral Code"
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# REFERRAL HISTORY
# =========================================

class ReferralHistoryView(APIView):

    def get(self, request, mobile):

        try:

            referrals = ReferralTransaction.objects.filter(

                inviter_mobile=mobile

            ).order_by("-created_at")

            data = []

            for r in referrals:

                data.append({

                    "invited_mobile":

                    r.invited_mobile,

                    "bonus":

                    r.bonus_amount,

                    "date":

                    r.created_at
                })

            return Response({

                "success": True,

                "history": data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# CUSTOMER REWARD DASHBOARD
# =========================================

class RewardDashboardView(APIView):

    def get(self, request, mobile):

        try:

            wallet = CustomerWallet.objects.get(

                customer_mobile=mobile
            )

            cashback_history = CashbackTransaction.objects.filter(

                customer_mobile=mobile

            ).order_by("-created_at")

            history = []

            for item in cashback_history:

                history.append({

                    "order_id":

                    item.order_id,

                    "cashback":

                    item.cashback_amount,

                    "reward_points":

                    item.reward_points,

                    "date":

                    item.created_at
                })

            return Response({

                "success": True,

                "wallet_balance":

                wallet.balance,

                "reward_points":

                wallet.reward_points,

                "vip_level":

                wallet.vip_level,

                "total_cashback":

                wallet.total_cashback_earned,

                "history":

                history
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
            
# =========================================
# AI FOOD RECOMMENDATION API
# =========================================

class AIRecommendationView(APIView):

    def get(self, request, mobile):

        try:

            recommendations = recommend_foods(

                mobile
            )

            return Response({

                "success": True,

                "recommendations":

                recommendations
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# CUSTOMER ANALYTICS DASHBOARD
# =========================================

class CustomerAnalyticsView(APIView):

    def get(self, request):

        try:

            # =====================================
            # TOTAL CUSTOMERS
            # =====================================

            total_customers = CustomerWallet.objects.count()

            # =====================================
            # ACTIVE CUSTOMERS
            # =====================================

            active_customers = Order.objects.values(

                'mobile'

            ).distinct().count()

            # =====================================
            # TOTAL ORDERS
            # =====================================

            total_orders = Order.objects.count()

            # =====================================
            # TOTAL REVENUE
            # =====================================

            total_revenue = Order.objects.aggregate(

                total=Sum('total_price')

            )['total'] or 0

            # =====================================
            # TOP CUSTOMERS
            # =====================================

            top_customers = Order.objects.values(

                'customer_name',
                'mobile'

            ).annotate(

                total_spent=Sum('total_price'),

                total_orders=Count('id')

            ).order_by('-total_spent')[:5]

            # =====================================
            # MONTHLY SALES
            # =====================================

            monthly_sales = Order.objects.annotate(

                month=TruncMonth('created_at')

            ).values('month').annotate(

                revenue=Sum('total_price'),

                orders=Count('id')

            ).order_by('month')

            # =====================================
            # MOST ORDERED FOODS
            # =====================================

            popular_foods = Order.objects.values(

                'food_name'

            ).annotate(

                total_orders=Count('id')

            ).order_by('-total_orders')[:5]

            # =====================================
            # RESPONSE
            # =====================================

            return Response({

                "success": True,

                "analytics": {

                    "total_customers":

                    total_customers,

                    "active_customers":

                    active_customers,

                    "total_orders":

                    total_orders,

                    "total_revenue":

                    total_revenue,

                    "top_customers":

                    top_customers,

                    "monthly_sales":

                    monthly_sales,

                    "popular_foods":

                    popular_foods
                }
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


class SaveFCMTokenView(APIView):

    def post(self, request):

        mobile = request.data.get(

            "mobile"
        )

        token = request.data.get(

            "token"
        )

        CustomerDevice.objects.update_or_create(

            customer_mobile=mobile,

            defaults={

                "fcm_token": token
            }
        )

        return Response({

            "success": True
        })
        
        
# =========================================
# ADMIN ANALYTICS DASHBOARD
# =========================================

class AdminAnalyticsView(APIView):

    def get(self, request):

        try:

            today = timezone.now().date()

            # =====================================
            # ORDER ANALYTICS
            # =====================================

            total_orders = Order.objects.count()

            completed_orders = Order.objects.filter(

                status="Delivered"

            ).count()

            cancelled_orders = Order.objects.filter(

                status="Cancelled"

            ).count()

            pending_orders = Order.objects.exclude(

                status__in=[

                    "Delivered",
                    "Cancelled"
                ]

            ).count()

            live_deliveries = Order.objects.filter(

                status="On The Way"

            ).count()

            # =====================================
            # REVENUE
            # =====================================

            total_revenue = Order.objects.filter(

                payment_status="Paid"

            ).aggregate(

                total=Sum("total_price")

            )["total"] or 0

            today_revenue = Order.objects.filter(

                created_at__date=today,

                payment_status="Paid"

            ).aggregate(

                total=Sum("total_price")

            )["total"] or 0

            today_orders = Order.objects.filter(

                created_at__date=today

            ).count()

            # =====================================
            # RIDERS
            # =====================================

            active_riders = Rider.objects.filter(

                is_available=False

            ).count()

            total_riders = Rider.objects.count()

            # =====================================
            # RESTAURANTS
            # =====================================

            total_restaurants = Restaurant.objects.count()

            active_restaurants = Restaurant.objects.filter(

                is_active=True

            ).count()

            # =====================================
            # RESPONSE
            # =====================================

            return Response({

                "success": True,

                "dashboard": {

                    "total_orders":
                    total_orders,

                    "completed_orders":
                    completed_orders,

                    "cancelled_orders":
                    cancelled_orders,

                    "pending_orders":
                    pending_orders,

                    "live_deliveries":
                    live_deliveries,

                    "total_revenue":
                    total_revenue,

                    "today_revenue":
                    today_revenue,

                    "today_orders":
                    today_orders,

                    "total_riders":
                    total_riders,

                    "active_riders":
                    active_riders,

                    "total_restaurants":
                    total_restaurants,

                    "active_restaurants":
                    active_restaurants
                }
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
            
# =========================================
# CUSTOMER NOTIFICATION CENTER
# =========================================

class CustomerNotificationView(APIView):

    def get(self, request):

        mobile = request.GET.get(

            "mobile"
        )

        notifications = CustomerNotification.objects.filter(

            customer_mobile=mobile

        ).order_by(

            "-created_at"
        )

        serializer = CustomerNotificationSerializer(

            notifications,

            many=True
        )

        return Response({

            "success": True,

            "notifications":

            serializer.data
        })



# =========================================
# MARK NOTIFICATION READ
# =========================================

class MarkNotificationReadView(APIView):

    def post(self, request):

        notification_id = request.data.get(

            "notification_id"
        )

        notification = CustomerNotification.objects.get(

            id=notification_id
        )

        notification.is_read = True

        notification.save()

        return Response({

            "success": True
        })


# =========================================
# CUSTOMER ORDER HISTORY
# =========================================

class CustomerOrderHistoryView(APIView):

    def get(self, request):

        try:

            mobile = request.GET.get(

                "mobile"
            )

            orders = Order.objects.filter(

                mobile=mobile

            ).order_by(

                "-id"
            )

            serializer = OrderSerializer(

                orders,

                many=True
            )

            total_orders = orders.count()

            delivered_orders = orders.filter(

                status="Delivered"

            ).count()

            cancelled_orders = orders.filter(

                status="Cancelled"

            ).count()

            active_orders = orders.exclude(

                status__in=[
                    "Delivered",
                    "Cancelled"
                ]
            ).count()

            total_spent = orders.filter(

                payment_status="Paid"

            ).aggregate(

                total=Sum("total_price")

            )["total"] or 0

            return Response({

                "success": True,

                "summary": {

                    "total_orders":
                    total_orders,

                    "delivered_orders":
                    delivered_orders,

                    "cancelled_orders":
                    cancelled_orders,

                    "active_orders":
                    active_orders,

                    "total_spent":
                    total_spent
                },

                "orders":

                serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
            

# =========================================
# CUSTOMER ORDER DETAIL
# =========================================

class CustomerOrderDetailView(APIView):

    def get(self, request, id):

        try:

            order = Order.objects.get(

                id=id
            )

            serializer = OrderSerializer(

                order
            )

            return Response({

                "success": True,

                "order":

                serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })
            
            
# =========================================
# CUSTOMER PROFILE
# =========================================

class CustomerProfileView(APIView):

    def get(self, request):

        try:

            mobile = request.GET.get(

                "mobile"
            )

            profile = CustomerProfile.objects.get(

                mobile=mobile
            )

            serializer = CustomerProfileSerializer(

                profile
            )

            return Response({

                "success": True,

                "profile":

                serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# UPDATE CUSTOMER PROFILE
# =========================================

class UpdateCustomerProfileView(APIView):

    parser_classes = [

        MultiPartParser,

        FormParser
    ]

    def post(self, request):

        try:

            mobile = request.data.get(

                "mobile"
            )

            profile = CustomerProfile.objects.get(

                mobile=mobile
            )

            profile.customer_name = request.data.get(

                "customer_name",

                profile.customer_name
            )

            profile.email = request.data.get(

                "email",

                profile.email
            )

            profile.address = request.data.get(

                "address",

                profile.address
            )

            if request.FILES.get(

                "profile_image"
            ):

                profile.profile_image = request.FILES.get(

                    "profile_image"
                )

            profile.save()

            return Response({

                "success": True,

                "message":

                "Profile Updated Successfully"
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# ADD CUSTOMER ADDRESS
# =========================================

class AddCustomerAddressView(APIView):

    def post(self, request):

        try:

            mobile = request.data.get(

                "customer_mobile"
            )

            if request.data.get(

                "is_default"
            ):

                CustomerAddress.objects.filter(

                    customer_mobile=mobile

                ).update(

                    is_default=False
                )

            address = CustomerAddress.objects.create(

                customer_mobile=mobile,

                address_type=request.data.get(

                    "address_type"
                ),

                full_address=request.data.get(

                    "full_address"
                ),

                landmark=request.data.get(

                    "landmark"
                ),

                latitude=request.data.get(

                    "latitude"
                ),

                longitude=request.data.get(

                    "longitude"
                ),

                is_default=request.data.get(

                    "is_default",

                    False
                )
            )

            return Response({

                "success": True,

                "address_id":

                address.id
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# CUSTOMER ADDRESS LIST
# =========================================

class CustomerAddressListView(APIView):

    def get(self, request):

        mobile = request.GET.get(

            "mobile"
        )

        addresses = CustomerAddress.objects.filter(

            customer_mobile=mobile

        ).order_by(

            "-is_default"
        )

        serializer = CustomerAddressSerializer(

            addresses,

            many=True
        )

        return Response({

            "success": True,

            "addresses":

            serializer.data
        })



# =========================================
# UPDATE ADDRESS
# =========================================

class UpdateCustomerAddressView(APIView):

    def post(self, request):

        try:

            address = CustomerAddress.objects.get(

                id=request.data.get(

                    "address_id"
                )
            )

            address.address_type = request.data.get(

                "address_type",

                address.address_type
            )

            address.full_address = request.data.get(

                "full_address",

                address.full_address
            )

            address.landmark = request.data.get(

                "landmark",

                address.landmark
            )

            address.save()

            return Response({

                "success": True
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# DELETE ADDRESS
# =========================================

class DeleteCustomerAddressView(APIView):

    def post(self, request):

        try:

            CustomerAddress.objects.filter(

                id=request.data.get(

                    "address_id"
                )

            ).delete()

            return Response({

                "success": True
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# CREATE SUPPORT TICKET
# =========================================

class CreateSupportTicketView(APIView):

    def post(self, request):

        try:

            ticket = SupportTicket.objects.create(

                customer_mobile=request.data.get(

                    "customer_mobile"
                ),

                order_id=request.data.get(

                    "order_id"
                ),

                subject=request.data.get(

                    "subject"
                ),

                message=request.data.get(

                    "message"
                )
            )

            return Response({

                "success": True,

                "ticket_id":

                ticket.id
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# CUSTOMER TICKETS
# =========================================

class CustomerSupportTicketsView(APIView):

    def get(self, request):

        mobile = request.GET.get(

            "mobile"
        )

        tickets = SupportTicket.objects.filter(

            customer_mobile=mobile

        ).order_by(

            "-id"
        )

        serializer = SupportTicketSerializer(

            tickets,

            many=True
        )

        return Response({

            "success": True,

            "tickets":

            serializer.data
        })



# =========================================
# ADD SUPPORT MESSAGE
# =========================================

class AddSupportMessageView(APIView):

    def post(self, request):

        try:

            message = SupportMessage.objects.create(

                ticket_id=request.data.get(

                    "ticket_id"
                ),

                sender=request.data.get(

                    "sender"
                ),

                message=request.data.get(

                    "message"
                )
            )

            return Response({

                "success": True,

                "message_id":

                message.id
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# TICKET DETAILS
# =========================================

class SupportTicketDetailView(APIView):

    def get(self, request, id):

        try:

            ticket = SupportTicket.objects.get(

                id=id
            )

            serializer = SupportTicketSerializer(

                ticket
            )

            return Response({

                "success": True,

                "ticket":

                serializer.data
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })


# =========================================
# SUBMIT FEEDBACK
# =========================================

class SubmitFeedbackView(APIView):

    def post(self, request):

        try:

            order = Order.objects.get(

                id=request.data.get(
                    "order_id"
                )
            )

            feedback = CustomerFeedback.objects.create(

                customer_mobile=request.data.get(
                    "customer_mobile"
                ),

                order=order,

                restaurant=order.restaurant,

                rider=order.assigned_rider,

                restaurant_rating=request.data.get(
                    "restaurant_rating"
                ),

                rider_rating=request.data.get(
                    "rider_rating"
                ),

                food_rating=request.data.get(
                    "food_rating"
                ),

                review=request.data.get(
                    "review"
                )
            )

            return Response({

                "success": True,

                "feedback_id":
                feedback.id
            })

        except Exception as e:

            return Response({

                "success": False,

                "error": str(e)
            })



# =========================================
# FEEDBACK HISTORY
# =========================================

class CustomerFeedbackHistoryView(APIView):

    def get(self, request):

        mobile = request.GET.get(

            "mobile"
        )

        feedbacks = CustomerFeedback.objects.filter(

            customer_mobile=mobile

        ).order_by(

            "-id"
        )

        serializer = CustomerFeedbackSerializer(

            feedbacks,

            many=True
        )

        return Response({

            "success": True,

            "feedbacks":

            serializer.data
        })



# =========================================
# RESTAURANT RATING ANALYTICS
# =========================================

class RestaurantRatingAnalyticsView(APIView):

    def get(self, request, id):

        ratings = CustomerFeedback.objects.filter(

            restaurant_id=id
        )

        return Response({

            "success": True,

            "restaurant_rating":

            ratings.aggregate(

                Avg("restaurant_rating")

            )["restaurant_rating__avg"],

            "food_rating":

            ratings.aggregate(

                Avg("food_rating")

            )["food_rating__avg"],

            "total_reviews":

            ratings.count()
        })



# =========================================
# RIDER RATING ANALYTICS
# =========================================

class RiderRatingAnalyticsView(APIView):

    def get(self, request, id):

        ratings = CustomerFeedback.objects.filter(

            rider_id=id
        )

        return Response({

            "success": True,

            "average_rating":

            ratings.aggregate(

                Avg("rider_rating")

            )["rider_rating__avg"],

            "total_reviews":

            ratings.count()
        })


