# =========================================
# AI SMART DELIVERY PRIORITY SYSTEM
# =========================================

from math import radians, sin, cos, sqrt, atan2


# =========================================
# DISTANCE CALCULATOR
# =========================================

def calculate_distance(lat1, lng1, lat2, lng2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)

    a = (

        sin(dlat / 2) ** 2 +

        cos(radians(lat1)) *

        cos(radians(lat2)) *

        sin(dlng / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# =========================================
# PRIORITY ENGINE
# =========================================

def calculate_priority(order):

    score = 0

    # =====================================
    # HIGH PRICE = HIGH PRIORITY
    # =====================================

    if order.total_price >= 1000:

        score += 50

    elif order.total_price >= 500:

        score += 30

    else:

        score += 10

    # =====================================
    # OLD ORDER = HIGH PRIORITY
    # =====================================

    if order.created_at:

        from django.utils.timezone import now

        minutes = (

            now() - order.created_at

        ).seconds / 60

        if minutes >= 30:

            score += 50

        elif minutes >= 15:

            score += 25

    # =====================================
    # LONG DISTANCE = HIGH PRIORITY
    # =====================================

    restaurant_lat = 23.0225
    restaurant_lng = 72.5714

    distance = calculate_distance(

        restaurant_lat,
        restaurant_lng,

        order.delivery_latitude,
        order.delivery_longitude
    )

    if distance >= 10:

        score += 40

    elif distance >= 5:

        score += 20

    # =====================================
    # FINAL PRIORITY
    # =====================================

    return {

        "score": score,
        "distance": round(distance, 2)
    }