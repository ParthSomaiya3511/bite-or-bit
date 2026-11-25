# =========================================
# AI ATTENDANCE SYSTEM
# =========================================

from django.utils import timezone

from orders.models import (

    RiderShift,
    RiderWallet
)


# =========================================
# CLOCK IN
# =========================================

def rider_clock_in(rider):

    shift = RiderShift.objects.create(

        rider=rider,

        clock_in=timezone.now(),

        attendance_status="Present"
    )

    return shift


# =========================================
# CLOCK OUT
# =========================================

def rider_clock_out(rider):

    shift = RiderShift.objects.filter(

        rider=rider,

        clock_out__isnull=True

    ).last()

    if not shift:

        return None

    shift.clock_out = timezone.now()

    duration = (

        shift.clock_out - shift.clock_in
    )

    hours = duration.total_seconds() / 3600

    shift.total_hours = round(hours, 2)

    # =====================================
    # PRODUCTIVITY SCORE
    # =====================================

    productivity = min(

        100,

        shift.total_hours * 12
    )

    shift.productivity_score = productivity

    # =====================================
    # OVERTIME
    # =====================================

    if shift.total_hours > 8:

        shift.overtime_hours = (

            shift.total_hours - 8
        )

    # =====================================
    # PEAK BONUS
    # =====================================

    bonus = 0

    if shift.total_hours >= 10:

        bonus = 300

    elif shift.total_hours >= 8:

        bonus = 150

    shift.peak_hour_bonus = bonus

    # =====================================
    # ADD BONUS TO WALLET
    # =====================================

    wallet, created = RiderWallet.objects.get_or_create(

        rider=rider
    )

    wallet.available_balance += bonus

    wallet.bonus += bonus

    wallet.save()

    shift.save()

    return {

        "hours":
        shift.total_hours,

        "productivity":
        shift.productivity_score,

        "bonus":
        bonus,

        "overtime":
        shift.overtime_hours
    }
