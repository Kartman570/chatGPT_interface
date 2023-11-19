async function sendMessage() {
    let messageInput = document.getElementById("messageInput");
    let message = messageInput.value;
    let chatBox = document.getElementById("chatBox");
    let loadingIndicator = document.getElementById("loading");
    let sendButton = document.getElementById("sendButton");

    // Добавляем сообщение пользователя в чат
    appendMessageToChatBox("Вы: " + message, "user-message");

    // Показать индикатор загрузки и скрыть кнопку отправки
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
            appendMessageToChatBox("Ошибка: " + response.status, "gpt-response");
        }
    } catch (error) {
        appendMessageToChatBox("Ошибка: " + error, "gpt-response");
    } finally {
        // Скрыть индикатор загрузки и включить кнопку отправки
        loadingIndicator.style.display = "none";
        sendButton.disabled = false;
        messageInput.value = ""; // Очистка поля ввода
        chatBox.scrollTop = chatBox.scrollHeight; // Прокрутка вниз к последнему сообщению
    }
}

function appendMessageToChatBox(message, className) {
    let chatBox = document.getElementById("chatBox");
    let messageDiv = document.createElement("div");
    messageDiv.className = "message " + className;
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
}
