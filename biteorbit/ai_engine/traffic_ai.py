# =========================================
# REAL AI TRAFFIC ENGINE
# =========================================

import random


# =========================================
# TRAFFIC LEVELS
# =========================================

TRAFFIC_LEVELS = [

    "Low",
    "Medium",
    "High",
    "Very High"
]


# =========================================
# AI TRAFFIC SIMULATION
# =========================================

def get_live_traffic(lat, lng):

    traffic = random.choice(

        TRAFFIC_LEVELS
    )

    # =====================================
    # TRAFFIC SPEED
    # =====================================

    if traffic == "Low":

        speed = 40
        delay = 0
        color = "green"

    elif traffic == "Medium":

        speed = 25
        delay = 5
        color = "orange"

    elif traffic == "High":

        speed = 15
        delay = 15
        color = "red"

    else:

        speed = 8
        delay = 30
        color = "darkred"

    return {

        "traffic_level": traffic,

        "speed_kmph": speed,

        "delay_minutes": delay,

        "color": color
    }


# =========================================
# SMART ETA ENGINE
# =========================================

def calculate_ai_eta(

    rider_lat,
    rider_lng,

    order_lat,
    order_lng
):

    # =====================================
    # DISTANCE
    # =====================================

    distance = abs(

        float(rider_lat)
        -
        float(order_lat)

    ) + abs(

        float(rider_lng)
        -
        float(order_lng)
    )

    distance = distance * 111

    # =====================================
    # TRAFFIC
    # =====================================

    traffic = get_live_traffic(

        order_lat,
        order_lng
    )

    speed = traffic["speed_kmph"]

    # =====================================
    # ETA
    # =====================================

    eta = (distance / speed) * 60

    eta += traffic["delay_minutes"]

    return {

        "eta_minutes": int(eta),

        "distance_km": round(distance, 2),

        "traffic": traffic
    }
