# =========================================
# AI WITHDRAW CHECK
# =========================================

def withdraw_ai_check(

    wallet_balance,
    withdraw_amount
):

    result = {

        "allowed": True,

        "reason": "Approved"
    }

    # =====================================
    # LOW BALANCE
    # =====================================

    if withdraw_amount > wallet_balance:

        result["allowed"] = False

        result["reason"] = "Insufficient Balance"

    # =====================================
    # MINIMUM RULE
    # =====================================

    elif withdraw_amount < 100:

        result["allowed"] = False

        result["reason"] = "Minimum ₹100 Required"

    # =====================================
    # HIGH RISK
    # =====================================

    elif withdraw_amount > 10000:

        result["allowed"] = False

        result["reason"] = "Large Withdrawal Detected"

    return result
