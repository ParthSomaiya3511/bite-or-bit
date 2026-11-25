
async function loadFraudOrders() {

    const response =
        await fetch(

            "http://127.0.0.1:8000/api/orders/fraud-orders/"
        )

    const data =
        await response.json()

    const container =
        document.getElementById(

            "fraud-container"
        )

    container.innerHTML = ""

    data.fraud_orders.forEach(order => {

        container.innerHTML += `

                <div class="fraud-card">

                    <h2>

                        🚨 Order #${order.id}

                    </h2>

                    <h4>

                        ${order.customer_name}

                    </h4>

                    <h5>

                        📞 ${order.mobile}

                    </h5>

                    <h5>

                        💰 ₹${order.amount}

                    </h5>

                    <h5 class="danger">

                        Fraud Score:
                        ${order.fraud_score}
                    </h5>

                    <p>

                        ${order.fraud_reason}

                    </p>

                </div>

                `
    })
}

loadFraudOrders()