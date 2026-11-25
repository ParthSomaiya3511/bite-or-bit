// =========================================
// ORDER ID
// =========================================

// const orderId = 1

const orderId =
    localStorage.getItem(
        "latest_order_id"
    )
// =========================================
// MAP
// =========================================

const map = L.map('map').setView(

    [23.0225, 72.5714],

    14
)

L.tileLayer(

    'https://tile.openstreetmap.org/{z}/{x}/{y}.png',

    {

        attribution:
            '&copy; OpenStreetMap'
    }

).addTo(map)


// =========================================
// RIDER MARKER
// =========================================

const riderIcon = L.icon({

    iconUrl:
        'https://cdn-icons-png.flaticon.com/512/2972/2972185.png',

    iconSize: [55, 55]
})

let riderMarker = L.marker(

    [23.0225, 72.5714],

    {

        icon: riderIcon
    }

).addTo(map)


// =========================================
// START LIVE TRACKING
// =========================================

function startTracking() {

    if (navigator.geolocation) {

        navigator.geolocation.watchPosition(

            async function(position) {

                const latitude =
                    position.coords.latitude

                const longitude =
                    position.coords.longitude

                console.log(

                    latitude,
                    longitude
                )

                // MOVE MARKER

                riderMarker.setLatLng([

                    latitude,
                    longitude
                ])

                map.panTo([

                    latitude,
                    longitude
                ])

                // SEND TO DJANGO

                await fetch(

                    "http://127.0.0.1:8000/api/orders/update-rider-location/",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                            "application/json"
                        },

                        body: JSON.stringify({

                            order_id: orderId,

                            latitude: latitude,

                            longitude: longitude
                        })
                    }
                )

            },

            function(error) {

                console.log(error)
            },

            {

                enableHighAccuracy: true
            }
        )

    } else {

        alert("GPS Not Supported")
    }
}
