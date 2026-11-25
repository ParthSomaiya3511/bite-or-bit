import razorpay
import stripe

from django.conf import settings

# =========================================
# RAZORPAY CLIENT
# =========================================

razorpay_client = razorpay.Client(

    auth=(

        settings.RAZORPAY_KEY_ID,

        settings.RAZORPAY_KEY_SECRET
    )
)

# =========================================
# STRIPE CONFIG
# =========================================

stripe.api_key = settings.STRIPE_SECRET_KEY
