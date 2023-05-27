function insertMessage(isUser, message) {
    const chatWindow = document.querySelector('.chat-window');
    const messageCard = document.createElement('div');
    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';
    const cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.textContent = message.includes(":") ? message.split(":")[0] + ":" : message;
    cardBody.appendChild(cardText);

    const laptops = message.split(":")[1];
    if (laptops) {
        const ul = document.createElement('ul');
        laptops.split("€").forEach((laptop) => {
            if (laptop.length > 2) {
                const li = document.createElement('li');
                li.textContent = laptop.trim() + " €";
                ul.appendChild(li);
            }
        });
        cardBody.appendChild(ul);
    }

    messageCard.appendChild(cardBody);
    messageCard.className = isUser ? 'card user-message' : 'card bot-message';
    chatWindow.appendChild(messageCard);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage() {
    const inputMessage = document.getElementById('input-message');
    const message = inputMessage.value.trim();

    if (message !== '') {
        insertMessage(true, message);
        inputMessage.value = '';
        await responseMessage(message);
    }
}

async function responseMessage(message) {
    try {
        const data = {"message": message};
        const resp = await axios.post('/api/message', data);
        const respMessage = resp.data.message.trim();
        if (respMessage !== '') {
            insertMessage(false, respMessage);
        }
    } catch (e) {
        console.log(e);
    }
}

function checkEnterKey(event) {
    if (event.keyCode === 13) {
        sendMessage();
    }
}
