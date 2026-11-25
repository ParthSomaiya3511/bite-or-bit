import math


# =========================================
# CALCULATE DISTANCE
# =========================================

def calculate_distance(

    lat1,
    lon1,

    lat2,
    lon2
):

    R = 6371

    dLat = math.radians(

        lat2 - lat1
    )

    dLon = math.radians(

        lon2 - lon1
    )

    a = (

        math.sin(dLat / 2) ** 2

        +

        math.cos(math.radians(lat1))

        *

        math.cos(math.radians(lat2))

        *

        math.sin(dLon / 2) ** 2
    )

    c = 2 * math.atan2(

        math.sqrt(a),

        math.sqrt(1 - a)
    )

    distance = R * c

    return round(distance, 2)


# =========================================
# ETA CALCULATOR
# =========================================

def calculate_eta(distance_km):

    avg_speed = 30

    eta_hours = distance_km / avg_speed

    eta_minutes = eta_hours * 60

    return round(eta_minutes)
