# =========================================
# AI SMART SCHEDULER
# =========================================

from datetime import time

from orders.models import (

    Rider,
    RiderSchedule,
    RiderPerformance
)


# =========================================
# GENERATE AI SHIFT
# =========================================

def generate_rider_schedule(rider):

    performance, created = RiderPerformance.objects.get_or_create(

        rider=rider
    )

    deliveries = performance.successful_deliveries

    # =====================================
    # AI SHIFT TYPE
    # =====================================

    if deliveries >= 200:

        shift_name = "Elite Peak Shift"

        shift_start = time(18, 0)

        shift_end = time(2, 0)

        peak = True

        priority = 100

    elif deliveries >= 100:

        shift_name = "Evening Shift"

        shift_start = time(14, 0)

        shift_end = time(22, 0)

        peak = True

        priority = 80

    else:

        shift_name = "Day Shift"

        shift_start = time(9, 0)

        shift_end = time(17, 0)

        peak = False

        priority = 60

    workload = deliveries * 0.5

    schedule = RiderSchedule.objects.create(

        rider=rider,

        shift_name=shift_name,

        shift_start=shift_start,

        shift_end=shift_end,

        assigned_orders=deliveries,

        workload_score=workload,

        ai_priority_score=priority,

        is_peak_shift=peak
    )

    return {

        "shift": shift_name,

        "priority": priority,

        "workload": workload
    }


# =========================================
# AI BEST RIDER SCHEDULER
# =========================================

def get_best_scheduled_rider():

    schedules = RiderSchedule.objects.filter(

        rider__is_available=True

    ).order_by(

        "-ai_priority_score",
        "workload_score"
    )

    if schedules.exists():

        return schedules.first().rider

    return None
