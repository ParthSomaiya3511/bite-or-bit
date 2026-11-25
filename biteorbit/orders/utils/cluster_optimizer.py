import uuid

from orders.models import Order

from .eta import calculate_distance


# =========================================
# FIND CLUSTER ORDERS
# =========================================

def find_cluster_orders(

    latitude,
    longitude
):

    nearby_orders = []

    pending_orders = Order.objects.filter(

        status="Preparing",

        assigned_rider__isnull=True
    )

    for order in pending_orders:

        if order.latitude and order.longitude:

            distance = calculate_distance(

                float(latitude),
                float(longitude),

                float(order.latitude),
                float(order.longitude)
            )

            # WITHIN 3 KM

            if distance <= 3:

                nearby_orders.append(order)

    return nearby_orders


# =========================================
# CREATE CLUSTER
# =========================================

def create_cluster(orders):

    cluster_id = str(uuid.uuid4())[:8]

    sequence = 1

    for order in orders:

        order.cluster_id = cluster_id

        order.delivery_sequence = sequence

        order.save()

        sequence += 1

    return cluster_id
