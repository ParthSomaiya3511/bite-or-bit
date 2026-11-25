# =========================================
# AI DELIVERY HEATMAP SYSTEM
# =========================================

from collections import defaultdict


# =========================================
# GENERATE HEATMAP
# =========================================

def generate_heatmap(orders):

    heatmap = defaultdict(int)

    for order in orders:

        lat = round(
            order.delivery_latitude,
            2
        )

        lng = round(
            order.delivery_longitude,
            2
        )

        key = f"{lat},{lng}"

        heatmap[key] += 1

    result = []

    for key, count in heatmap.items():

        lat, lng = key.split(",")

        result.append({

            "latitude": float(lat),

            "longitude": float(lng),

            "count": count
        })

    return result