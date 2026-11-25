# =========================================
# AI FOOD RECOMMENDATION ENGINE
# =========================================

from collections import Counter

from orders.models import (
    Order,
    FoodItem
)

# =========================================
# GET CUSTOMER FOOD HISTORY
# =========================================

def get_customer_preferences(

    customer_mobile
):

    orders = Order.objects.filter(

        mobile=customer_mobile

    ).order_by("-id")

    food_names = []

    for order in orders:

        if order.food_name:

            food_names.append(

                order.food_name
            )

    return Counter(food_names)

# =========================================
# AI RECOMMENDATION
# =========================================

def recommend_foods(

    customer_mobile
):

    preferences = get_customer_preferences(

        customer_mobile
    )

    top_foods = preferences.most_common(3)

    recommended = []

    # =====================================
    # AI SIMILAR FOOD SEARCH
    # =====================================

    for food_name, _ in top_foods:

        foods = FoodItem.objects.filter(

            name__icontains=food_name[:3]

        )[:3]

        for food in foods:

            recommended.append({

                "id": food.id,

                "name": food.name,

                "price": food.price,

                "image": food.image.url if food.image else None
            })

    return recommended
