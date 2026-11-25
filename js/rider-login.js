const API_BASE =
    "http://127.0.0.1:8000"


// =========================================
// LOGIN FORM
// =========================================

document
    .getElementById("login-form")

    .addEventListener(

        "submit",

        async function (e) {

            e.preventDefault()

            const email =
                document.getElementById(
                    "email"
                ).value

            const password =
                document.getElementById(
                    "password"
                ).value

            try {

                const response =
                    await fetch(

                        "http://127.0.0.1:8000/api/orders/rider-login/",

                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                email,
                                password
                            })
                        }
                    )

                const data =
                    await response.json()

                console.log(data)

                // SUCCESS

                if (data.success) {

                    // SAVE LOGIN

                    localStorage.setItem(

                        "rider_logged_in",

                        "true"
                    )

                    localStorage.setItem(

                        "rider_id",

                        data.rider_id
                    )

                    localStorage.setItem(

                        "rider_name",

                        data.name
                    )

                    localStorage.setItem(

                        "rider_email",

                        data.email
                    )

                    // TOAST

                    showToast(
                        "✅ Login Successful"
                    )

                    // REDIRECT

                    setTimeout(() => {

                        window.location.href =
                            "rider-dashboard.html"

                    }, 1500)
                }

                // ERROR

                else {

                    showToast(
                        "❌ " + data.message
                    )
                }

            } catch (error) {

                console.log(error)

                showToast(
                    "❌ Server Error"
                )
            }
        }
    )
