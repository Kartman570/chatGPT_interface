async function sendMessage() {
    let message = document.getElementById("messageInput").value;
    let responseParagraph = document.getElementById("response");
    let loadingIndicator = document.getElementById("loading");
    let sendButton = document.getElementById("sendButton");

    loadingIndicator.style.display = "inline-block";
    sendButton.disabled = true;

    try {
        let response = await fetch('http://18.198.189.134:8000/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (response.ok) {
            let data = await response.json();
            responseParagraph.textContent = "Ответ GPT: " + data.response;
        } else {
            responseParagraph.textContent = "Ошибка: " + response.status;
        }
    } catch (error) {
        responseParagraph.textContent = "Ошибка: " + error;
    } finally {
        loadingIndicator.style.display = "none";
        sendButton.disabled = false;
    }
}
