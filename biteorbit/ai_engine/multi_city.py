# =========================================
# REAL AI MULTI CITY SYSTEM
# =========================================

from orders.models import Rider


# =========================================
# CITY ZONES
# =========================================

CITY_ZONES = {

    "Ahmedabad": {

        "lat_range": (22.90, 23.20),

        "lng_range": (72.40, 72.70)
    },

    "Mumbai": {

        "lat_range": (18.90, 19.30),

        "lng_range": (72.75, 73.10)
    },

    "Delhi": {

        "lat_range": (28.40, 28.90),

        "lng_range": (76.80, 77.30)
    }
}


# =========================================
# DETECT CITY
# =========================================

def detect_city(lat, lng):

    for city, zone in CITY_ZONES.items():

        if (

            zone["lat_range"][0]
            <= float(lat)
            <= zone["lat_range"][1]

            and

            zone["lng_range"][0]
            <= float(lng)
            <= zone["lng_range"][1]
        ):

            return city

    return "Unknown"


# =========================================
# GET CITY RIDERS
# =========================================

def get_city_riders(city):

    riders = Rider.objects.filter(

        is_available=True
    )

    city_riders = []

    for rider in riders:

        rider_city = detect_city(

            rider.latitude,
            rider.longitude
        )

        if rider_city == city:

            city_riders.append(rider)

    return city_riders


# =========================================
# BEST CITY RIDER
# =========================================

def get_best_city_rider(order_lat, order_lng):

    city = detect_city(

        order_lat,
        order_lng
    )

    riders = get_city_riders(city)

    if not riders:

        return {

            "city": city,

            "rider": None
        }

    best_rider = None

    min_distance = 999999

    for rider in riders:

        distance = abs(

            rider.latitude - float(order_lat)

        ) + abs(

            rider.longitude - float(order_lng)
        )

        if distance < min_distance:

            min_distance = distance

            best_rider = rider

    return {

        "city": city,

        "rider": best_rider
    }
