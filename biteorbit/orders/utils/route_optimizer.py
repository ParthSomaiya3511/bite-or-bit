from orders.models import Rider

from .eta import (

    calculate_distance,

    calculate_eta
)


# =========================================
# FIND BEST RIDER
# =========================================

def find_best_rider(

    customer_lat,
    customer_lon
):

    available_riders = Rider.objects.filter(

        is_online=True,

        is_busy=False
    )

    best_rider = None

    shortest_distance = 999999

    best_eta = 0

    for rider in available_riders:

        distance = calculate_distance(

            float(rider.latitude),
            float(rider.longitude),

            float(customer_lat),
            float(customer_lon)
        )

        eta = calculate_eta(
            distance
        )

        if distance < shortest_distance:

            shortest_distance = distance

            best_rider = rider

            best_eta = eta

    return {

        "rider": best_rider,

        "distance": shortest_distance,

        "eta": best_eta
    }
