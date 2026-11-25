const btn = document.getElementById("voice-btn");
const status = document.getElementById("status");

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.lang = "en-US";
recognition.continuous = false;

btn.onclick = () => {
    status.innerText = "Listening... 🎤";
    recognition.start();
};

recognition.onresult = async (event) => {

    const text =
        event.results[0][0].transcript.toLowerCase();

    status.innerText = "You said: " + text;

    if (
        text.includes("help") ||
        text.includes("emergency") ||
        text.includes("accident")
    ) {
        triggerSOS();
    }
};

async function triggerSOS() {

    navigator.geolocation.getCurrentPosition(async (pos) => {

        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        const res = await fetch(
            "/api/sos/voice-sos/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    latitude: lat,
                    longitude: lng,
                    message: "VOICE SOS DETECTED",
                    emergency_type: "Voice Emergency"
                })
            }
        );

        const data = await res.json();

        alert(data.message);

    });

}

recognition.onerror = () => {
    status.innerText = "Voice error, try again";
};
