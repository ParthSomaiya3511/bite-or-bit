async function loadDemand() {

    const response =
        await fetch(

            "http://127.0.0.1:8000/api/orders/predict-demand/"
        )

    const data =
        await response.json()

    const container =
        document.getElementById(

            "demand-container"
        )

    container.innerHTML = ""

    data.prediction.forEach(item => {

        let colorClass = "low"

        if (item.demand === "High") {

            colorClass = "high"
        }

        else if (item.demand === "Medium") {

            colorClass = "medium"
        }

        container.innerHTML += `

                <div class="demand-card">

                    <h3>

                        📍 Area:
                        ${item.area}

                    </h3>

                    <h4>

                        Orders:
                        ${item.total_orders}

                    </h4>

                    <h5 class="${colorClass}">

                        Demand:
                        ${item.demand}

                    </h5>

                </div>

                `
    })
}

loadDemand()
