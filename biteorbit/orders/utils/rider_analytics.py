# =========================================
# AI SMART RIDER PERFORMANCE ANALYTICS
# =========================================

from orders.models import Rider
from orders.models import Order


# =========================================
# ANALYTICS
# =========================================

def rider_performance_analytics():

    riders = Rider.objects.all()

    analytics = []

    for rider in riders:

        orders = Order.objects.filter(

            assigned_rider=rider
        )

        total_orders = orders.count()

        delivered_orders = orders.filter(

            status="Delivered"
        ).count()

        cancelled_orders = orders.filter(

            status="Cancelled"
        ).count()

        pending_orders = orders.exclude(

            status="Delivered"
        ).count()

        # =====================================
        # SUCCESS RATE
        # =====================================

        success_rate = 0

        if total_orders > 0:

            success_rate = round(

                (delivered_orders / total_orders) * 100,

                2
            )

        # =====================================
        # AI PERFORMANCE SCORE
        # =====================================

        performance = "Poor"

        if success_rate >= 90:

            performance = "Excellent"

        elif success_rate >= 70:

            performance = "Good"

        elif success_rate >= 50:

            performance = "Average"

        analytics.append({

            "rider_id": rider.id,

            "rider_name": rider.name,

            "total_orders": total_orders,

            "delivered_orders": delivered_orders,

            "cancelled_orders": cancelled_orders,

            "pending_orders": pending_orders,

            "success_rate": success_rate,

            "performance": performance
        })

    return analytics