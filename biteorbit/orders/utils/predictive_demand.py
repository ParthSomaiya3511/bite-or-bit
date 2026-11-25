# =========================================
# AI PREDICTIVE DELIVERY DEMAND SYSTEM
# =========================================

from collections import defaultdict

from orders.models import Order


# =========================================
# PREDICT DEMAND
# =========================================

def predict_delivery_demand():

    orders = Order.objects.all()

    area_count = defaultdict(int)

    # =====================================
    # COUNT ORDERS AREA WISE
    # =====================================

    for order in orders:

        lat = round(
            order.delivery_latitude,
            1
        )

        lng = round(
            order.delivery_longitude,
            1
        )

        key = f"{lat},{lng}"

        area_count[key] += 1

    result = []

    # =====================================
    # DEMAND ANALYSIS
    # =====================================

    for area, total_orders in area_count.items():

        demand = "Low"

        if total_orders >= 10:

            demand = "High"

        elif total_orders >= 5:

            demand = "Medium"

        result.append({

            "area": area,

            "total_orders": total_orders,

            "demand": demand
        })

    # SORT HIGH TO LOW

    result = sorted(

        result,

        key=lambda x: x["total_orders"],

        reverse=True
    )

    return result