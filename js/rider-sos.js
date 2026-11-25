// =========================================
// EMERGENCY SOS SYSTEM
// =========================================

const sosBtn = document.getElementById(

    "sos-btn"
)

// =========================================
// CLICK EVENT
// =========================================

if(sosBtn){

    sosBtn.onclick = async () => {

        // CONFIRM

        const confirmSOS = confirm(

            "Are you sure you want to send Emergency SOS?"
        )

        if(!confirmSOS){

            return
        }

        // LOADING

        sosBtn.innerHTML =
        "Sending SOS..."

        sosBtn.disabled = true

        // GET GPS

        navigator.geolocation.getCurrentPosition(

            async(position) => {

                try{

                    const lat =
                    position.coords.latitude

                    const lng =
                    position.coords.longitude

                    // API CALL

                    const response = await fetch(

                        "http://127.0.0.1:8000/api/orders/create-sos/",

                        {

                            method:"POST",

                            headers:{

                                "Content-Type":
                                "application/json"
                            },

                            body:JSON.stringify({

                                rider_id:1,

                                order_id:1,

                                latitude:lat,

                                longitude:lng,

                                emergency_type:

                                "Accident",

                                message:

                                "Rider needs emergency help immediately"
                            })
                        }
                    )

                    const data =
                    await response.json()

                    // SUCCESS

                    if(data.success){

                        sosBtn.innerHTML =
                        "🚨 SOS SENT"

                        sosBtn.style.background =
                        "#00c853"

                        alert(

                            "Emergency Alert Sent Successfully"
                        )

                    }else{

                        throw new Error(
                            data.error
                        )
                    }

                }catch(error){

                    console.log(error)

                    alert(

                        "Failed To Send SOS"
                    )

                    sosBtn.innerHTML =
                    "🚨 EMERGENCY SOS"

                    sosBtn.disabled = false
                }

            },

            () => {

                alert(

                    "Location Permission Required"
                )

                sosBtn.innerHTML =
                "🚨 EMERGENCY SOS"

                sosBtn.disabled = false
            }
        )
    }
}