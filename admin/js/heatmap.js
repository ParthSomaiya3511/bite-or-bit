// =========================================
// MAP
// =========================================

const map = L.map("map").setView(

    [23.0225, 72.5714],

    12
)

// =========================================
// TILE
// =========================================

L.tileLayer(

    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

    {

        attribution:
        "BiteOrbit AI"
    }

).addTo(map)

// =========================================
// LOAD HEATMAP
// =========================================

async function loadHeatmap(){

    try{

        const response = await fetch(

            "http://127.0.0.1:8000/api/orders/delivery-heatmap/"
        )

        const data = await response.json()

        const heatPoints = []

        data.data.forEach(point => {

            heatPoints.push([

                point.lat,
                point.lng,
                point.weight
            ])
        })

        L.heatLayer(

            heatPoints,

            {

                radius:35,
                blur:25,
                maxZoom:17
            }

        ).addTo(map)

    }

    catch(error){

        console.log(error)
    }
}

// =========================================
// INIT
// =========================================

loadHeatmap()
