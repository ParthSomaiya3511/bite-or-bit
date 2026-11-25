# =========================================
# AI AUTO ORDER BATCHING SYSTEM
# =========================================

from collections import defaultdict

from orders.models import Order


# =========================================
# CREATE ORDER BATCHES
# =========================================

def create_order_batches():

    orders = Order.objects.filter(

        status="Preparing",

        assigned_rider__isnull=True
    )

    batches = defaultdict(list)

    # =====================================
    # GROUP BY AREA
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

        batches[key].append(order)

    result = []

    # =====================================
    # CREATE BATCH
    # =====================================

    for key, batch_orders in batches.items():

        if len(batch_orders) >= 2:

            result.append({

                "area": key,

                "orders": [

                    order.id
                    for order in batch_orders
                ],

                "count": len(batch_orders)
            })

    return result