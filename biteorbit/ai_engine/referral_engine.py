import random
import string

# =========================================
# GENERATE REFERRAL CODE
# =========================================

def generate_referral_code(name):

    prefix = name[:3].upper()

    random_number = random.randint(

        1000,
        9999
    )

    return f"{prefix}{random_number}"
