from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    customer_name = models.CharField(max_length=255)

    mobile = models.CharField(max_length=20)

    address = models.TextField()

    city = models.CharField(max_length=100)

    pincode = models.CharField(max_length=20)

    payment_method = models.CharField(max_length=50)
    
    coupon_code = models.CharField(

        max_length=50,
        null=True,
        blank=True
    )

    discount_amount = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    
    fcm_token = models.TextField(
        null=True,
        blank=True
    )
    
    restaurant = models.ForeignKey(

        'Restaurant',

        on_delete=models.CASCADE,

        null=True,
        blank=True
    )


    delivery_latitude = models.FloatField(
        default=23.0300
    )

    delivery_longitude = models.FloatField(
        default=72.5800
    )

    base_delivery_fee = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=30
    )

    surge_multiplier = models.FloatField(
        default=1
    )

    final_delivery_fee = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=30
    )

    pricing_reason = models.TextField(
        null=True,
        blank=True
    )

    STATUS_CHOICES = (

        ("Pending", "Pending"),
        ("Preparing", "Preparing"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    
    delivery_boy = models.ForeignKey(

        'DeliveryBoy',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assigned_rider = models.ForeignKey(

        'Rider',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    
    latitude = models.FloatField( 
        null=True, 
        blank=True 
    ) 
    
    longitude = models.FloatField( 
        null=True, 
        blank=True 
    )
    
    rider_lat = models.FloatField(
        null=True,
        blank=True
    )

    rider_lng = models.FloatField(
        null=True,
        blank=True
    )
    
    eta_minutes = models.IntegerField(
        default=0
    )
    
    is_accepted = models.BooleanField( 
        default=False 
    ) 
    
    cluster_id = models.CharField(

        max_length=100,

        null=True,

        blank=True
    )
    
    traffic_level = models.CharField(

        max_length=100,

        null=True,

        blank=True
    )

    delivery_sequence = models.IntegerField(

        default=1
    )
    
    is_fraud = models.BooleanField(
        default=False
    )

    fraud_score = models.IntegerField(
        default=0
    )

    fraud_reason = models.TextField(
        null=True,
        blank=True
    )
    
    accepted_at = models.DateTimeField( 
        null=True, 
        blank=True 
    )
    
    payment_method = models.CharField(

        max_length=50,
        default="COD"
    )

    payment_status = models.CharField(

        max_length=50,
        default="Pending"
    )

    wallet_paid_amount = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=0
    )

    cashback_amount = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.customer_name
    
    
# =========================================
# CUSTOMER WALLET
# =========================================

class CustomerWallet(models.Model):

    customer_name = models.CharField(
        max_length=255
    )

    customer_mobile = models.CharField(
        max_length=20,
        unique=True
    )

    balance = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=0
    )

    
    referral_code = models.CharField(

        max_length=20,

        unique=True,

        null=True,

        blank=True
    )

    referred_by = models.CharField(

        max_length=20,

        null=True,

        blank=True
    )

    total_referral_earnings = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=0
    )

    reward_points = models.IntegerField(
        default=0
    )

    total_cashback_earned = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=0
    )

    vip_level = models.CharField(

        max_length=50,
        default="Bronze"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.customer_name} - ₹{self.balance}"


# =========================================
# WALLET TRANSACTIONS
# =========================================

class WalletTransaction(models.Model):

    TRANSACTION_TYPES = (

        ("credit", "Credit"),
        ("debit", "Debit"),
        ("cashback", "Cashback"),
        ("refund", "Refund")
    )

    wallet = models.ForeignKey(

        CustomerWallet,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(

        max_digits=10,
        decimal_places=2
    )

    transaction_type = models.CharField(

        max_length=20,
        choices=TRANSACTION_TYPES
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.wallet.customer_name} - {self.transaction_type}"
    


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    food_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    image = models.TextField(blank=True, null=True)


class Payment(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    razorpay_order_id = models.CharField(
        max_length=255
    )

    razorpay_payment_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    razorpay_signature = models.TextField(
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=50,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.razorpay_order_id
    
    
class DeliveryLocation(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    latitude = models.FloatField(default=0)

    longitude = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"{self.order.id}"
    
    
    
# =========================================
# DELIVERY BOY MODEL
# =========================================

class DeliveryBoy(models.Model):

    name = models.CharField(
        max_length=255
    )

    email = models.EmailField(
        unique=True
    )

    mobile = models.CharField(
        max_length=20
    )

    password = models.CharField(
        max_length=255
    )

    bike_number = models.CharField(
        max_length=50
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name
    
    
# =========================================
# DELIVERY RIDER MODEL
# =========================================

class Rider(models.Model):

    name = models.CharField(
        max_length=200
    )

    mobile = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        null=True,
        blank=True
    )

    password = models.CharField( 
        max_length=255, 
        null=True, 
        blank=True 
    )

    profile_image = models.ImageField(
        upload_to="riders/",
        blank=True,
        null=True
    )

    vehicle_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    latitude = models.FloatField(
        default=23.0300
    )

    longitude = models.FloatField(
        default=72.5800
    )

    is_available = models.BooleanField(
        default=True
    )
    
    # =========================================
    # AI MOOD + STRESS SYSTEM
    # =========================================

    stress_level = models.IntegerField(
        default=0
    )

    mood_status = models.CharField(
        max_length=50,
        default="Normal"
    )

    fatigue_score = models.IntegerField(
        default=0
    )

    mental_health_score = models.IntegerField(
        default=100
    )

    last_break_time = models.DateTimeField(
        null=True,
        blank=True
    )

    anger_reports = models.IntegerField(
        default=0
    )

    late_delivery_count = models.IntegerField(
        default=0
    )

    safety_score = models.IntegerField(
        default=100
    )

    is_in_accident = models.BooleanField(
        default=False
    )

    overspeed_count = models.IntegerField(
        default=0
    )

    sudden_brake_count = models.IntegerField(
        default=0
    )

    last_speed = models.FloatField(
        default=0
    )

    emergency_mode = models.BooleanField(
        default=False
    )

    last_location_update = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name

    
# ========================================= 
# # CHAT MODEL 
# # ========================================= 

class ChatMessage(models.Model): 
    order = models.ForeignKey( 
        Order, 
        on_delete=models.CASCADE, 
        related_name="messages" 
    ) 
    
    sender = models.CharField( 
        max_length=20 
    ) 
    
    message = models.TextField() 
    
    created_at = models.DateTimeField( 
        auto_now_add=True 
    ) 
    
    def __str__(self): 
        return f"{self.sender} - {self.order.id}"
    
    
# =========================================
# RIDER WALLET MODEL
# =========================================

class RiderWallet(models.Model):

    rider = models.OneToOneField(

        Rider,
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    total_earnings = models.FloatField(
        default=0
    )

    available_balance = models.FloatField(
        default=0
    )

    completed_orders = models.IntegerField(
        default=0
    )

    today_earnings = models.FloatField(
        default=0
    )

    weekly_earnings = models.FloatField(
        default=0
    )

    monthly_earnings = models.FloatField(
        default=0
    )

    bonus = models.FloatField(
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.rider.name



# =========================================
# RIDER WITHDRAW MODEL
# =========================================

class RiderWithdraw(models.Model):

    STATUS_CHOICES = (

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected")
    )

    rider = models.ForeignKey(

        Rider,
        on_delete=models.CASCADE,
        related_name="withdraws"
    )

    amount = models.FloatField()

    payment_method = models.CharField(
        max_length=50
    )

    upi_id = models.CharField(

        max_length=255,
        null=True,
        blank=True
    )

    bank_name = models.CharField(

        max_length=255,
        null=True,
        blank=True
    )

    account_number = models.CharField(

        max_length=255,
        null=True,
        blank=True
    )

    ifsc_code = models.CharField(

        max_length=100,
        null=True,
        blank=True
    )

    status = models.CharField(

        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    admin_note = models.TextField(

        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.rider.name} - {self.amount}"



# =========================================
# RIDER BONUS HISTORY
# =========================================

class RiderBonus(models.Model):

    rider = models.ForeignKey(

        Rider,
        on_delete=models.CASCADE,
        related_name="bonuses"
    )

    bonus_type = models.CharField(
        max_length=100
    )

    amount = models.FloatField(
        default=0
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.rider.name} - {self.bonus_type}"


# =========================================
# RIDER PERFORMANCE MODEL
# =========================================

class RiderPerformance(models.Model):

    rider = models.OneToOneField(

        Rider,
        on_delete=models.CASCADE,
        related_name="performance"
    )

    total_deliveries = models.IntegerField(
        default=0
    )

    successful_deliveries = models.IntegerField(
        default=0
    )

    failed_deliveries = models.IntegerField(
        default=0
    )

    fraud_reports = models.IntegerField(
        default=0
    )

    average_eta = models.FloatField(
        default=0
    )

    performance_score = models.FloatField(
        default=0
    )

    rider_rank = models.CharField(

        max_length=50,
        default="Bronze"
    )
    
    xp_points = models.IntegerField(
        default=0
    )

    level = models.IntegerField(
        default=1
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.rider.name


# =========================================
# RIDER ACHIEVEMENT MODEL
# =========================================

class RiderAchievement(models.Model):

    rider = models.ForeignKey(

        Rider,
        on_delete=models.CASCADE,
        related_name="achievements"
    )

    badge_name = models.CharField(
        max_length=255
    )

    badge_icon = models.CharField(
        max_length=255
    )

    description = models.TextField()

    xp_reward = models.IntegerField(
        default=0
    )

    unlocked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.rider.name} - {self.badge_name}"


# =========================================
# RIDER MISSION MODEL
# =========================================

class RiderMission(models.Model):

    rider = models.ForeignKey(

        Rider,
        on_delete=models.CASCADE,
        related_name="missions"
    )

    mission_title = models.CharField(
        max_length=255
    )

    mission_description = models.TextField()

    target_count = models.IntegerField(
        default=0
    )

    completed_count = models.IntegerField(
        default=0
    )

    reward_amount = models.FloatField(
        default=0
    )

    xp_reward = models.IntegerField(
        default=0
    )

    is_completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    def __str__(self):

        return self.mission_title


# =========================================
# RIDER STREAK MODEL
# =========================================

class RiderStreak(models.Model):

    rider = models.OneToOneField(

        Rider,
        on_delete=models.CASCADE,
        related_name="streak"
    )

    current_streak = models.IntegerField(
        default=0
    )

    highest_streak = models.IntegerField(
        default=0
    )

    total_xp = models.IntegerField(
        default=0
    )

    rider_level = models.IntegerField(
        default=1
    )

    streak_multiplier = models.FloatField(
        default=1.0
    )

    last_delivery_date = models.DateField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.rider.name


# =========================================
# RIDER DISCIPLINE MODEL
# =========================================

class RiderDiscipline(models.Model):

    rider = models.OneToOneField(

        Rider,
        on_delete=models.CASCADE,
        related_name="discipline"
    )

    warning_count = models.IntegerField(
        default=0
    )

    late_delivery_count = models.IntegerField(
        default=0
    )

    fraud_count = models.IntegerField(
        default=0
    )

    cancelled_delivery_count = models.IntegerField(
        default=0
    )

    trust_score = models.FloatField(
        default=100
    )

    reputation_level = models.CharField(

        max_length=50,
        default="Excellent"
    )

    is_suspended = models.BooleanField(
        default=False
    )

    suspension_reason = models.TextField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.rider.name


# =========================================
# RIDER SHIFT MODEL
# =========================================

class RiderShift(models.Model):

    rider = models.ForeignKey(

        Rider,
        on_delete=models.CASCADE,
        related_name="shifts"
    )

    clock_in = models.DateTimeField(
        null=True,
        blank=True
    )

    clock_out = models.DateTimeField(
        null=True,
        blank=True
    )

    total_hours = models.FloatField(
        default=0
    )

    attendance_status = models.CharField(

        max_length=50,
        default="Absent"
    )

    productivity_score = models.FloatField(
        default=0
    )

    overtime_hours = models.FloatField(
        default=0
    )

    peak_hour_bonus = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.rider.name


# =========================================
# RIDER SCHEDULE MODEL
# =========================================

class RiderSchedule(models.Model):

    rider = models.ForeignKey(

        Rider,
        on_delete=models.CASCADE,
        related_name="schedules"
    )

    shift_name = models.CharField(
        max_length=100
    )

    shift_start = models.TimeField()

    shift_end = models.TimeField()

    assigned_orders = models.IntegerField(
        default=0
    )

    workload_score = models.FloatField(
        default=0
    )

    ai_priority_score = models.FloatField(
        default=0
    )

    is_peak_shift = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.rider.name} - {self.shift_name}"



# =========================================
# RIDER FATIGUE LOG
# =========================================

class RiderFatigue(models.Model):

    rider = models.ForeignKey(
        Rider,
        on_delete=models.CASCADE,
        related_name="fatigue_logs"
    )

    fatigue_score = models.IntegerField(
        default=0
    )

    working_hours = models.FloatField(
        default=0
    )

    completed_orders = models.IntegerField(
        default=0
    )

    rest_hours = models.FloatField(
        default=0
    )

    is_fatigued = models.BooleanField(
        default=False
    )

    fatigue_reason = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.rider.name} - {self.fatigue_score}"


class RiderSOS(models.Model):

    rider = models.ForeignKey(
        'Rider',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    emergency_type = models.CharField(
        max_length=100,
        default="Unknown"
    )

    message = models.TextField(
        default="No message provided",
        blank=True
    )

    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOS - {self.id}"
    
    

# =========================================
# RESTAURANT MODEL
# =========================================

class Restaurant(models.Model):

    name = models.CharField(
        max_length=255
    )

    owner_name = models.CharField(
        max_length=255
    )

    email = models.EmailField(
        unique=True
    )

    mobile = models.CharField(
        max_length=20
    )

    password = models.CharField(
        max_length=255
    )

    logo = models.ImageField(

        upload_to="restaurants/",

        null=True,
        blank=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    latitude = models.FloatField(
        default=23.0225
    )

    longitude = models.FloatField(
        default=72.5714
    )

    delivery_radius = models.FloatField(
        default=10
    )

    is_open = models.BooleanField(
        default=True
    )

    rating = models.FloatField(
        default=5
    )

    total_orders = models.IntegerField(
        default=0
    )

    total_earnings = models.DecimalField(

        max_digits=12,
        decimal_places=2,

        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================================
# RESTAURANT OWNER
# =========================================

class RestaurantOwner(models.Model):

    restaurant = models.OneToOneField(

        'Restaurant',

        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=255
    )

    mobile = models.CharField(
        max_length=20
    )

    profile_image = models.ImageField(

        upload_to="restaurant_owner/",

        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================================
# FOOD MODEL
# =========================================

class Food(models.Model):

    restaurant = models.ForeignKey(

        Restaurant,
        on_delete=models.CASCADE,
        related_name="foods"
    )

    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="foods/",
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================================
# PAYMENT TRANSACTION
# =========================================

class PaymentTransaction(models.Model):

    order = models.ForeignKey(

        Order,

        on_delete=models.CASCADE,

        related_name="payments"
    )

    payment_id = models.CharField(

        max_length=255,

        blank=True,
        null=True
    )

    razorpay_order_id = models.CharField(

        max_length=255,

        blank=True,
        null=True
    )

    razorpay_signature = models.TextField(

        blank=True,
        null=True
    )

    amount = models.DecimalField(

        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(

        max_length=100,

        default="Razorpay"
    )

    status = models.CharField(

        max_length=50,

        default="Pending"
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return str(self.order.id)


# =========================================
# MEMBERSHIP PLAN
# =========================================

class MembershipPlan(models.Model):

    PLAN_TYPES = (

        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum")
    )

    name = models.CharField(
        max_length=100
    )

    plan_type = models.CharField(

        max_length=50,
        choices=PLAN_TYPES
    )

    price = models.DecimalField(

        max_digits=10,
        decimal_places=2
    )

    duration_days = models.IntegerField()

    free_delivery = models.BooleanField(
        default=False
    )

    priority_delivery = models.BooleanField(
        default=False
    )

    cashback_percent = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================================
# CUSTOMER MEMBERSHIP
# =========================================

class CustomerMembership(models.Model):

    customer_name = models.CharField(
        max_length=255
    )

    customer_mobile = models.CharField(
        max_length=20
    )

    plan = models.ForeignKey(

        MembershipPlan,
        on_delete=models.CASCADE
    )

    start_date = models.DateTimeField(
        auto_now_add=True
    )

    expiry_date = models.DateTimeField()

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return f"{self.customer_name} - {self.plan.name}"


# =========================================
# COUPON SYSTEM
# =========================================

class Coupon(models.Model):

    COUPON_TYPES = (

        ("percentage", "Percentage"),
        ("fixed", "Fixed")
    )

    code = models.CharField(

        max_length=50,
        unique=True
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    coupon_type = models.CharField(

        max_length=20,
        choices=COUPON_TYPES
    )

    discount_value = models.DecimalField(

        max_digits=10,
        decimal_places=2
    )

    minimum_order_amount = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=0
    )

    maximum_discount = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    usage_limit = models.IntegerField(
        default=100
    )

    used_count = models.IntegerField(
        default=0
    )

    expiry_date = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.code


# =========================================
# REFERRAL TRANSACTION
# =========================================

class ReferralTransaction(models.Model):

    inviter_mobile = models.CharField(
        max_length=20
    )

    invited_mobile = models.CharField(
        max_length=20
    )

    referral_code = models.CharField(
        max_length=20
    )

    bonus_amount = models.DecimalField(

        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.referral_code


# =========================================
# CASHBACK HISTORY
# =========================================

class CashbackTransaction(models.Model):

    customer_mobile = models.CharField(
        max_length=20
    )

    order_id = models.IntegerField()

    cashback_amount = models.DecimalField(

        max_digits=10,
        decimal_places=2
    )

    reward_points = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.customer_mobile


class FoodItem(models.Model):

    restaurant = models.ForeignKey(

        Restaurant,

        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    price = models.DecimalField(

        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(

        upload_to="foods/",

        null=True,
        blank=True
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


class CustomerDevice(models.Model):

    customer_mobile = models.CharField(

        max_length=20
    )

    fcm_token = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True
    )
    
    
# =========================================
# CUSTOMER NOTIFICATIONS
# =========================================

class CustomerNotification(models.Model):

    customer_mobile = models.CharField(

        max_length=20
    )

    title = models.CharField(

        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(

        default=False
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return self.title


# =========================================
# CUSTOMER PROFILE
# =========================================

class CustomerProfile(models.Model):

    customer_name = models.CharField(

        max_length=255
    )

    mobile = models.CharField(

        max_length=20,

        unique=True
    )

    email = models.EmailField(

        null=True,

        blank=True
    )

    profile_image = models.ImageField(

        upload_to="customer_profiles/",

        null=True,

        blank=True
    )

    address = models.TextField(

        null=True,

        blank=True
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return self.customer_name


# =========================================
# CUSTOMER ADDRESS BOOK
# =========================================

class CustomerAddress(models.Model):

    customer_mobile = models.CharField(

        max_length=20
    )

    address_type = models.CharField(

        max_length=50,

        default="Home"
    )

    full_address = models.TextField()

    landmark = models.CharField(

        max_length=255,

        null=True,

        blank=True
    )

    latitude = models.FloatField(

        null=True,

        blank=True
    )

    longitude = models.FloatField(

        null=True,

        blank=True
    )

    is_default = models.BooleanField(

        default=False
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return f"{self.customer_mobile} - {self.address_type}"



# =========================================
# CUSTOMER SUPPORT TICKET
# =========================================

class SupportTicket(models.Model):

    TICKET_STATUS = (

        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Closed", "Closed")
    )

    customer_mobile = models.CharField(

        max_length=20
    )

    order = models.ForeignKey(

        Order,

        on_delete=models.CASCADE,

        null=True,

        blank=True
    )

    subject = models.CharField(

        max_length=255
    )

    message = models.TextField()

    status = models.CharField(

        max_length=50,

        choices=TICKET_STATUS,

        default="Open"
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return self.subject



# =========================================
# SUPPORT TICKET CHAT
# =========================================

class SupportMessage(models.Model):

    ticket = models.ForeignKey(

        SupportTicket,

        on_delete=models.CASCADE,

        related_name="messages"
    )

    sender = models.CharField(

        max_length=50
    )  # Customer/Admin

    message = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return self.sender



# =========================================
# CUSTOMER FEEDBACK
# =========================================

class CustomerFeedback(models.Model):

    customer_mobile = models.CharField(
        max_length=20
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    rider = models.ForeignKey(
        Rider,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    restaurant_rating = models.IntegerField(
        default=5
    )

    rider_rating = models.IntegerField(
        default=5
    )

    food_rating = models.IntegerField(
        default=5
    )

    review = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.customer_mobile
