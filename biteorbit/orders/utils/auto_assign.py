# =========================================
# AI AUTO RIDER ASSIGNMENT
# =========================================

from orders.models import Rider

from math import radians, sin, cos, sqrt, atan2


# =========================================
# DISTANCE CALCULATOR
# =========================================

def calculate_distance(

    lat1,
    lng1,

    lat2,
    lng2
):

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
# FIND BEST RIDER
# =========================================

def auto_assign_rider(order):

    riders = Rider.objects.filter(

        is_available=True
    )

    best_rider = None

    min_distance = 999999

    for rider in riders:

        distance = calculate_distance(

            rider.latitude,
            rider.longitude,

            order.delivery_latitude,
            order.delivery_longitude
        )

        if distance < min_distance:

            min_distance = distance

            best_rider = rider

    # =====================================
    # ASSIGN RIDER
    # =====================================

    if best_rider:

        order.assigned_rider = best_rider

        order.status = "Preparing"

        order.save()

        best_rider.is_available = False

        best_rider.save()

        return {

            "success": True,

            "rider": best_rider.name,

            "distance": round(
                min_distance,
                2
            )
        }

    return {

        "success": False,

        "message":
        "No Rider Available"
    }