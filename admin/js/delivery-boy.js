// =========================================
// LOAD RIDER ORDERS
// =========================================

async function loadOrders() {

    try {

        const response = await fetch(

            "http://127.0.0.1:8000/api/orders/admin-orders/"
        )

        const orders = await response.json()

        console.log(orders)

        let html = ""

        let completed = 0

        let earnings = 0

        orders.forEach(order => {

            if (
                order.status === "Out For Delivery"
                ||
                order.status === "Preparing"
            ) {

                html += `

                    <div class="order-card">

                        <div class="row">

                            <div class="col-md-8">

                                <h4>

                                    Order #${order.id}

                                </h4>

                                <p>

                                    ${order.customer_name}

                                </p>

                                <p>

                                    ${order.address}

                                </p>

                                <p>

                                    ₹ ${order.total_price}

                                </p>

                            </div>

                            <div class="col-md-4 text-end">

                                <span class="badge bg-success p-2">

                                    ${order.status}

                                </span>

                                <br><br>

                                <button
                                    class="btn btn-custom"
                                    onclick="markDelivered(${order.id})">

                                    Mark Delivered
                                </button>

                            </div>

                        </div>

                    </div>
                `
            }

            if (order.status === "Delivered") {

                completed++

                earnings += parseFloat(order.total_price)
            }
        })

        document.getElementById(

            "orders-container"

        ).innerHTML = html

        document.getElementById(

            "today-orders"

        ).innerHTML = orders.length

        document.getElementById(

            "completed-orders"

        ).innerHTML = completed

        document.getElementById(

            "today-earnings"

        ).innerHTML = earnings

    } catch (error) {

        console.log(error)
    }
}


// =========================================
// MARK DELIVERED
// =========================================

async function markDelivered(orderId) {

    try {

        await fetch(

            `http://127.0.0.1:8000/api/orders/update-status/${orderId}/`,

            {

                method: "PATCH",

                headers: {

                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({

                    status: "Delivered"
                })
            }
        )

        alert("Order Delivered ✅")

        loadOrders()

    } catch (error) {

        console.log(error)
    }
}


// =========================================
// AUTO LOAD
// =========================================

loadOrders()

setInterval(() => {

    loadOrders()

}, 5000)
