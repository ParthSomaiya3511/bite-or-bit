const orderId =
localStorage.getItem(
    "active_order_id"
)

const socket =
new WebSocket(

    `ws://127.0.0.1:8000/ws/tracking/${orderId}/`
)

socket.onopen = () => {

    console.log(
        "Tracking Connected"
    )

    startTracking()
}

function startTracking(){

    navigator.geolocation.watchPosition(

        position => {

            const lat =
            position.coords.latitude

            const lng =
            position.coords.longitude

            socket.send(

                JSON.stringify({

                    lat: lat,

                    lng: lng
                })
            )
        },

        error => {

            console.log(error)
        },

        {

            enableHighAccuracy:true
        }
    )
}