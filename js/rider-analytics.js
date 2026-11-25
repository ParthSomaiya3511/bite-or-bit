
async function loadAnalytics() {

    const response =
        await fetch(

            "http://127.0.0.1:8000/api/orders/rider-analytics/"
        )

    const data =
        await response.json()

    const container =
        document.getElementById(

            "analytics-container"
        )

    container.innerHTML = ""

    data.analytics.forEach(item => {

        let performanceClass = "poor"

        if (item.performance === "Excellent") {

            performanceClass = "excellent"
        }

        else if (item.performance === "Good") {

            performanceClass = "good"
        }

        else if (item.performance === "Average") {

            performanceClass = "average"
        }

        container.innerHTML += `

                <div class="analytics-card">

                    <h2>

                        🛵 ${item.rider_name}

                    </h2>

                    <h5>

                        Total Orders:
                        ${item.total_orders}

                    </h5>

                    <h5>

                        Delivered:
                        ${item.delivered_orders}

                    </h5>

                    <h5>

                        Cancelled:
                        ${item.cancelled_orders}

                    </h5>

                    <h5>

                        Pending:
                        ${item.pending_orders}

                    </h5>

                    <h4>

                        Success Rate:
                        ${item.success_rate}%
                    </h4>

                    <h3 class="${performanceClass}">

                        ${item.performance}

                    </h3>

                </div>

                `
    })
}

loadAnalytics()
