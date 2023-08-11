function sendMessage(messageContent) {
    console.debug("sendMessage", {messageContent})
}


export function initRoom(roomName, messageInput) {
    console.debug("initRoom", {roomName, messageInput})

    messageInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            const message = messageInput.value;
            messageInput.value = '';
            sendMessage(message);
        }
    })
}