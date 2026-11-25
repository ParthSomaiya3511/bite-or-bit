// =========================================
// GET ORDER ID
// =========================================

const params =

    new URLSearchParams(
        window.location.search
    )

const orderId =
    params.get("order_id")

// SHOW ORDER ID

document.getElementById(

    "success-order-id"

).innerHTML = orderId

// TRACK BUTTON

document.getElementById(

    "track-btn"

).href =

    `track-order.html?order_id=${orderId}`

// TOAST

showToast(
    "🎉 Order Confirmed"
)
