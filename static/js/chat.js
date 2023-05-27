function insertMessage(isUser, message, messages) {
    const chatWindow = document.querySelector('.chat-window');
    // Create a new message card
    const messageCard = document.createElement('div');
    // Create a new card body
    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';
    // Create a new card text
    const cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.textContent = message;
    // Append card text to card body
    cardBody.appendChild(cardText);
    if (messages) {
        // Creates a list with all messages and inserts it inside cardBody
        const messageList = document.createElement('ul');
        messageList.className = 'list-group';

        messages.forEach((msg) => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item';
            listItem.textContent = msg;
            messageList.appendChild(listItem);
        });

        cardBody.appendChild(messageList);
    }

    // Append message card to chat window
    chatWindow.appendChild(messageCard);
    // Append card body to message card
    messageCard.appendChild(cardBody);
    if (isUser) {
        messageCard.className = 'card user-message';
    } else {
        messageCard.className = 'card bot-message'
    }
    chatWindow.scrollTop = chatWindow.scrollHeight;

}

function sendMessage() {
    const inputMessage = document.getElementById('input-message');
    const message = inputMessage.value;

    if (message.trim() !== '') {
        insertMessage(true, message)
        // Clear input message
        inputMessage.value = '';
        // Scroll to the bottom of the chat window
        responseMessage(message);
    }

}

async function responseMessage(message) {
    try {

        const data = {
            "message": message
        }
        const resp = await axios.post('/api/message', data)
        const respMessage = resp.data.message
        const messages = resp.data.messages
        if (respMessage.trim() !== '') {
            if (messages) {
                insertMessage(false, respMessage, messages)
            }
        }
    } catch (e) {
        console.log(e)
    }
}

function checkEnterKey(event) {
    if (event.keyCode === 13) {
        sendMessage();
    }
}