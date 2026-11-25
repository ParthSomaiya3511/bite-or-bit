from datetime import timedelta
from django.utils import timezone

from orders.models import (
    Order,
    RiderFatigue
)

# =========================================
# AI FATIGUE DETECTOR
# =========================================

def detect_rider_fatigue(rider):

    now = timezone.now()

    today = now.date()

    # =====================================
    # TODAY ORDERS
    # =====================================

    today_orders = Order.objects.filter(

        assigned_rider=rider,

        created_at__date=today,

        status="Delivered"
    )

    completed_orders = today_orders.count()

    # =====================================
    # WORKING HOURS
    # =====================================

    first_order = today_orders.order_by(
        "created_at"
    ).first()

    last_order = today_orders.order_by(
        "-created_at"
    ).first()

    working_hours = 0

    if first_order and last_order:

        diff = (
            last_order.created_at -
            first_order.created_at
        )

        working_hours = round(

            diff.total_seconds() / 3600,
            2
        )

    # =====================================
    # REST HOURS
    # =====================================

    rest_hours = max(

        0,
        24 - working_hours
    )

    # =====================================
    # FATIGUE SCORE
    # =====================================

    fatigue_score = 0

    reasons = []

    # =====================================
    # DELIVERY COUNT
    # =====================================

    if completed_orders >= 20:

        fatigue_score += 40

        reasons.append(
            "Too many deliveries"
        )

    # =====================================
    # LONG WORKING HOURS
    # =====================================

    if working_hours >= 10:

        fatigue_score += 40

        reasons.append(
            "Working too long"
        )

    # =====================================
    # LOW REST
    # =====================================

    if rest_hours <= 6:

        fatigue_score += 20

        reasons.append(
            "Very low rest"
        )

    # =====================================
    # NIGHT SHIFT
    # =====================================

    current_hour = now.hour

    if current_hour >= 1 and current_hour <= 5:

        fatigue_score += 20

        reasons.append(
            "Late night exhaustion"
        )

    # =====================================
    # FATIGUE STATUS
    # =====================================

    is_fatigued = fatigue_score >= 60

    # =====================================
    # SAVE LOG
    # =====================================

    RiderFatigue.objects.create(

        rider=rider,

        fatigue_score=fatigue_score,

        working_hours=working_hours,

        completed_orders=completed_orders,

        rest_hours=rest_hours,

        is_fatigued=is_fatigued,

        fatigue_reason=", ".join(reasons)
    )

    # =====================================
    # AUTO BLOCK
    # =====================================

    if is_fatigued:

        rider.is_available = False

        rider.save()

    return {

        "fatigue_score": fatigue_score,

        "working_hours": working_hours,

        "completed_orders": completed_orders,

        "rest_hours": rest_hours,

        "is_fatigued": is_fatigued,

        "reasons": reasons
    }
