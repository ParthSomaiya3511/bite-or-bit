// =========================================
// LOAD SOS ALERTS
// =========================================

async function loadSOSAlerts(){

    const response = await fetch(

        "http://127.0.0.1:8000/api/orders/get-sos/"
    )

    const data = await response.json()

    const container =
    document.getElementById(

        "sos-container"
    )

    container.innerHTML = ""

    data.forEach((sos) => {

        container.innerHTML += `

        <div class="sos-card">

            <h2>

                🚨 ${sos.rider.name}

            </h2>

            <p>

                Emergency:
                ${sos.emergency_type}
            </p>

            <p>

                ${sos.message}
            </p>

            <p>

                GPS:
                ${sos.latitude},
                ${sos.longitude}
            </p>

            <button class="resolve-btn">

                Resolve
            </button>

        </div>
        `
    })
}

// AUTO REFRESH

setInterval(

    loadSOSAlerts,

    5000
)

loadSOSAlerts()