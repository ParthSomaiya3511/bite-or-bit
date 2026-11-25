# =========================================
# RIDER WALLET AI SYSTEM
# =========================================

from orders.models import RiderWallet


def update_rider_wallet(

    rider,
    order_amount
):

    # =====================================
    # GET OR CREATE WALLET
    # =====================================

    wallet, created = RiderWallet.objects.get_or_create(

        rider=rider
    )

    # =====================================
    # DELIVERY COMMISSION
    # =====================================

    earning = float(order_amount) * 0.20

    # =====================================
    # BONUS
    # =====================================

    bonus = 0

    if wallet.completed_orders >= 10:

        bonus = 100

    # =====================================
    # UPDATE WALLET
    # =====================================

    wallet.total_earnings += earning

    wallet.available_balance += earning

    wallet.completed_orders += 1

    wallet.today_earnings += earning

    wallet.weekly_earnings += earning

    wallet.monthly_earnings += earning

    wallet.bonus += bonus

    wallet.save()

    return {

        "earning": earning,

        "bonus": bonus,

        "wallet_balance":
        wallet.available_balance
    }
