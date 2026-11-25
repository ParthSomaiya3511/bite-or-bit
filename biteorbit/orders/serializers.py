from rest_framework import serializers

from .models import Order, OrderItem, DeliveryLocation, Rider, RiderSOS, Restaurant, RestaurantOwner, Food, CustomerWallet, WalletTransaction, MembershipPlan, CustomerMembership, Coupon, CustomerNotification, CustomerProfile, CustomerAddress, SupportTicket, SupportMessage, CustomerFeedback


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    assigned_rider_name = serializers.CharField(

        source="assigned_rider.name",

        read_only=True
    )
    
    rider_name = serializers.SerializerMethodField() 
    
    class Meta: 
        model = Order 
        fields = "__all__" 
    
    def get_rider_name(self, obj): 
        
        if obj.assigned_rider: 
            return obj.assigned_rider.name 
        
        return "Not Assigned"


class DeliveryLocationSerializer(serializers.ModelSerializer):

    class Meta:

        model = DeliveryLocation

        fields = "__all__"
        

class RiderSerializer(serializers.ModelSerializer): 
    
    class Meta: 
        
        model = Rider 
        
        fields = "__all__"
        
        

# =========================================
# RIDER SOS SERIALIZER
# =========================================

class RiderSOSSerializer(serializers.ModelSerializer):

    class Meta:

        model = RiderSOS

        fields = "__all__"
        
        
# =========================================
# RESTAURANT SERIALIZER
# =========================================

class RestaurantSerializer(

    serializers.ModelSerializer
):

    class Meta:

        model = Restaurant

        fields = "__all__"
        
        
        
# =========================================
# RESTAURANT OWNER SERIALIZER
# =========================================

class RestaurantOwnerSerializer(

    serializers.ModelSerializer
):

    class Meta:

        model = RestaurantOwner

        fields = "__all__"


# =========================================
# FOOD SERIALIZER
# =========================================

class FoodSerializer(serializers.ModelSerializer):

    class Meta:

        model = Food

        fields = "__all__"
        
        

# =========================================
# CUSTOMER WALLET SERIALIZER
# =========================================

class CustomerWalletSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomerWallet

        fields = "__all__"


# =========================================
# WALLET TRANSACTION SERIALIZER
# =========================================

class WalletTransactionSerializer(serializers.ModelSerializer):

    class Meta:

        model = WalletTransaction

        fields = "__all__"


# =========================================
# MEMBERSHIP PLAN SERIALIZER
# =========================================

class MembershipPlanSerializer(serializers.ModelSerializer):

    class Meta:

        model = MembershipPlan

        fields = "__all__"


# =========================================
# CUSTOMER MEMBERSHIP SERIALIZER
# =========================================

class CustomerMembershipSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomerMembership

        fields = "__all__"



# =========================================
# COUPON SERIALIZER
# =========================================

class CouponSerializer(serializers.ModelSerializer):

    class Meta:

        model = Coupon

        fields = "__all__"
        
        
class CustomerNotificationSerializer(

    serializers.ModelSerializer
):

    class Meta:

        model = CustomerNotification

        fields = "__all__"


class CustomerProfileSerializer(

    serializers.ModelSerializer
):

    class Meta:

        model = CustomerProfile

        fields = "__all__"


class CustomerAddressSerializer(

    serializers.ModelSerializer
):

    class Meta:

        model = CustomerAddress

        fields = "__all__"


class SupportMessageSerializer(

    serializers.ModelSerializer
):

    class Meta:

        model = SupportMessage

        fields = "__all__"


class SupportTicketSerializer(

    serializers.ModelSerializer
):

    messages = SupportMessageSerializer(

        many=True,

        read_only=True
    )

    class Meta:

        model = SupportTicket

        fields = "__all__"


class CustomerFeedbackSerializer(

    serializers.ModelSerializer
):

    class Meta:

        model = CustomerFeedback

        fields = "__all__"
