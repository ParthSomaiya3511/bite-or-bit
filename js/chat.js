const orderId = 35

const sender = "customer"

const chatBox =
    document.getElementById(
        "chat-messages"
    )


// =========================================
// LOAD CHAT
// =========================================

async function loadChat(){

    const response =
        await fetch(

            `http://127.0.0.1:8000/api/orders/chat/${orderId}/`
        )

    const data =
        await response.json()

    chatBox.innerHTML = ""

    data.forEach(msg => {

        chatBox.innerHTML += `

        <div class="message ${msg.sender}">

            ${msg.message}

        </div>
        `
    })

    chatBox.scrollTop =
        chatBox.scrollHeight
}


// =========================================
// SEND MESSAGE
// =========================================

document
    .getElementById("send-btn")

    .addEventListener(

        "click",

        async function(){

            const input =
                document.getElementById(
                    "chat-input"
                )

            const message =
                input.value

            if(message === "") return

            await fetch(

                "http://127.0.0.1:8000/api/orders/chat/send/",

                {

                    method:"POST",

                    headers:{

                        "Content-Type":
                            "application/json"
                    },

                    body:JSON.stringify({

                        order_id:orderId,

                        sender:sender,

                        message:message
                    })
                }
            )

            input.value = ""

            loadChat()
        }
    )


// =========================================
// AUTO REFRESH
// =========================================

setInterval(() => {

    loadChat()

}, 1000)

loadChat()



const socket =
    new WebSocket(

        `ws://127.0.0.1:8000/ws/chat/${orderId}/`
    )

socket.onmessage = function(e){

    const data = JSON.parse(e.data)

    addMessage(

        data.message,

        data.sender
    )
}


document
    .getElementById("send-btn")

    .addEventListener(

        "click",

        function(){

            const input =
                document.getElementById(
                    "chat-input"
                )

            const message =
                input.value

            socket.send(JSON.stringify({

                message: message,

                sender: "customer"
            }))

            input.value = ""
        }
    )


function addMessage(message, sender){

    const box =
        document.getElementById(
            "chat-messages"
        )

    box.innerHTML += `

        <div class="chat-message ${sender}">

            ${message}

        </div>
    `

    box.scrollTop =
        box.scrollHeight
}