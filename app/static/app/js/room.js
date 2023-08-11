async function sendMessage(roomName, messageContent) {
    console.debug("sendMessage", { messageContent })

    response = await fetch("/graphql", {
        method: "POST",
        body: JSON.stringify({
            query: `
                mutation sendMessage($roomName: String!, $messageContent: String!) {
                    sendChatRoomMessage(input: {
                        roomName: $roomName,
                        messageContent: $messageContent,
                    }) {
                        __typename
                    }
                }
            `,
            variables: {
                roomName, messageContent
            }
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    console.debug("sendMessage", { response })
}


export function initRoom(roomName, messageInput) {
    console.debug("initRoom", { roomName, messageInput })

    messageInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            const message = messageInput.value;
            messageInput.value = '';
            sendMessage(roomName, message);
        }
    })
}