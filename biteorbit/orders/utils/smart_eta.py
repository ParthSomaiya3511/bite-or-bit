# =========================================
# IMPORTS
# =========================================

import random
import math


# =========================================
# CALCULATE DISTANCE
# =========================================

def calculate_distance(

    lat1,
    lng1,
    lat2,
    lng2
):

    return math.sqrt(

        (lat2 - lat1) ** 2 +

        (lng2 - lng1) ** 2
    ) * 111


# =========================================
# AI SMART ETA
# =========================================

def smart_delivery_eta(

    rider_lat,
    rider_lng,

    customer_lat,
    customer_lng
):

    # =====================================
    # DISTANCE
    # =====================================

    distance = calculate_distance(

        rider_lat,
        rider_lng,

        customer_lat,
        customer_lng
    )

    # =====================================
    # AI TRAFFIC
    # =====================================

    traffic_factor = random.randint(1, 5)

    # =====================================
    # AI WEATHER
    # =====================================

    weather_factor = random.randint(0, 3)

    # =====================================
    # RIDER SPEED
    # =====================================

    rider_speed = random.randint(

        25,
        45
    )

    # =====================================
    # ETA FORMULA
    # =====================================

    eta = (

        distance / rider_speed
    ) * 60

    eta += traffic_factor * 2

    eta += weather_factor * 3

    # =====================================
    # MINIMUM ETA
    # =====================================

    eta = max(eta, 10)

    # =====================================
    # RESPONSE
    # =====================================

    return {

        "distance_km": round(distance, 2),

        "traffic_level": traffic_factor,

        "weather_level": weather_factor,

        "rider_speed": rider_speed,

        "predicted_eta": round(eta)
    }
