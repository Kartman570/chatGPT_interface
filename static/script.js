async function sendMessage() {
    let messageInput = document.getElementById("messageInput");
    let message = messageInput.value;
    let chatBox = document.getElementById("chatBox");
    let loadingIndicator = document.getElementById("loading");
    let sendButton = document.getElementById("sendButton");

    appendMessageToChatBox("You: " + message, "user-message");

    loadingIndicator.style.display = "inline-block";
    sendButton.disabled = true;

    try {
        let baseUrl = window.location.origin;
        let response = await fetch(baseUrl + '/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'message': message })
        });

        if (response.ok) {
            let data = await response.json();
            appendMessageToChatBox("GPT: " + data.response, "gpt-response");
        } else {
            appendMessageToChatBox("Error: " + response.status, "gpt-response");
        }
    } catch (error) {
        appendMessageToChatBox("Error: " + error, "gpt-response");
    } finally {
        loadingIndicator.style.display = "none";
        sendButton.disabled = false;
        messageInput.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

function appendMessageToChatBox(message, className) {
    let chatBox = document.getElementById("chatBox");
    let messageDiv = document.createElement("div");
    messageDiv.className = "message " + className;
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
}
