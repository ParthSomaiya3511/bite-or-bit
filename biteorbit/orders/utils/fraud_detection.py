# =========================================
# AI FRAUD DETECTION SYSTEM
# =========================================

from orders.models import Order


# =========================================
# DETECT FRAUD
# =========================================

def detect_fraud(order):

    fraud_score = 0

    fraud_reasons = []


    # =====================================
    # HIGH VALUE ORDER
    # =====================================

    if order.total_price > 5000:

        fraud_score += 30

        fraud_reasons.append(

            "High value order"
        )


    # =====================================
    # TOO MANY CANCELLED ORDERS
    # =====================================

    cancelled_orders = Order.objects.filter(

        mobile=order.mobile,

        status="Cancelled"
    ).count()

    if cancelled_orders >= 3:

        fraud_score += 40

        fraud_reasons.append(

            "Too many cancelled orders"
        )


    # =====================================
    # TOO MANY ORDERS SAME DAY
    # =====================================

    same_day_orders = Order.objects.filter(

        mobile=order.mobile
    ).count()

    if same_day_orders >= 10:

        fraud_score += 20

        fraud_reasons.append(

            "Too many orders detected"
        )


    # =====================================
    # INVALID ADDRESS
    # =====================================

    if len(order.address) < 10:

        fraud_score += 20

        fraud_reasons.append(

            "Invalid address"
        )


    # =====================================
    # FINAL AI RESULT
    # =====================================

    is_fraud = False

    if fraud_score >= 50:

        is_fraud = True


    return {

        "fraud_score": fraud_score,

        "is_fraud": is_fraud,

        "reasons": fraud_reasons
    }