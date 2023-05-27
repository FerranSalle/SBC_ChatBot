async function sendMessage() {
    const inputMessage = document.getElementById('input-message');
    const message = inputMessage.value;
    try {

        const data = {
            "message": message
        }
      await axios.post('/api/message', data)
    }catch (e) {
        console.log(e)
    }
    /*const inputMessage = document.getElementById('input-message');
    const message = inputMessage.value;

    if (message.trim() !== '') {
        const chatWindow = document.querySelector('.chat-window');

        // Create a new message card
        const messageCard = document.createElement('div');
        messageCard.className = 'card user-message';

        // Create a new card body
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';

        // Create a new card text
        const cardText = document.createElement('p');
        cardText.className = 'card-text';
        cardText.textContent = message;

        // Append card text to card body
        cardBody.appendChild(cardText);

        // Append card body to message card
        messageCard.appendChild(cardBody);

        // Append message card to chat window
        chatWindow.appendChild(messageCard);

        // Clear input message
        inputMessage.value = '';

        // Scroll to the bottom of the chat window
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }*/
}

function checkEnterKey(event) {
    if (event.keyCode === 13) {
        sendMessage();
    }
}