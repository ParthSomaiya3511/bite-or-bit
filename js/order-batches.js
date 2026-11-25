async function loadBatches() {

    const response =
        await fetch(

            "http://127.0.0.1:8000/api/orders/order-batches/"
        )

    const data =
        await response.json()

    const container =
        document.getElementById(

            "batch-container"
        )

    container.innerHTML = ""

    data.batches.forEach(batch => {

        container.innerHTML += `

                <div class="batch-card">

                    <h3>

                        📍 Area:
                        ${batch.area}

                    </h3>

                    <h5>

                        Total Orders:
                        ${batch.count}

                    </h5>

                    <p>

                        Orders:
                        ${batch.orders.join(", ")}

                    </p>

                </div>

                `
    })
}

loadBatches()
