// =========================================
// CREATE LOADER
// =========================================

document.addEventListener(

    "DOMContentLoaded",

    () => {

        let loader =
        document.getElementById(
            "loader-container"
        )

        // AUTO CREATE

        if(!loader){

            loader =
            document.createElement("div")

            loader.id =
            "loader-container"

            document.body.appendChild(
                loader
            )
        }

        loader.innerHTML = `

        <div class="loader-box">

            <div class="loader-ring"></div>

            <div class="loader-text">

                BiteOrbit

            </div>

            <div class="loader-sub">

                Loading Experience...

            </div>

        </div>

        `
    }
)

// =========================================
// HIDE LOADER
// =========================================

window.addEventListener(

    "load",

    () => {

        setTimeout(() => {

            const loader =
            document.getElementById(
                "loader-container"
            )

            if(loader){

                loader.classList.add(
                    "loader-hide"
                )
            }

        },1500)
    }
)