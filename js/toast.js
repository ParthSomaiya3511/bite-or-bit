// =========================================
// ULTRA PREMIUM TOAST
// =========================================

function showToast(

    message,

    type = "success"
){

    let toastBox =
    document.getElementById(
        "toast-box"
    )

    // AUTO CREATE

    if(!toastBox){

        toastBox =
        document.createElement("div")

        toastBox.id =
        "toast-box"

        document.body.appendChild(
            toastBox
        )
    }

    // ICONS

    let icon = "ℹ️"

    if(type === "success"){

        icon = "✅"
    }

    else if(type === "error"){

        icon = "❌"
    }

    else if(type === "info"){

        icon = "🚀"
    }

    // CREATE

    const toast =
    document.createElement("div")

    toast.className =

    `toast-item toast-${type}`

    toast.innerHTML = `

        <div class="toast-icon">

            ${icon}

        </div>

        <div class="toast-text">

            ${message}

        </div>
    `

    // APPEND

    toastBox.appendChild(
        toast
    )

    // REMOVE

    setTimeout(() => {

        toast.remove()

    },4500)
}