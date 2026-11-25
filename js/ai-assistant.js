// =========================================
// AI ASSISTANT SAFE LOAD
// =========================================

window.addEventListener(

    "DOMContentLoaded",

    () => {

        const toggleBtn =
            document.getElementById(
                "ai-toggle"
            )

        const closeBtn =
            document.getElementById(
                "ai-close"
            )

        const assistant =
            document.getElementById(
                "ai-assistant-box"
            )

        // SAFETY CHECK

        if (!toggleBtn || !assistant) {

            console.log(
                "AI Assistant Elements Missing"
            )

            return
        }

        // OPEN

        toggleBtn.onclick = () => {

            assistant.classList.add(
                "active"
            )
        }

        // CLOSE

        if (closeBtn) {

            closeBtn.onclick = () => {

                assistant.classList.remove(
                    "active"
                )
            }
        }
    }
)
