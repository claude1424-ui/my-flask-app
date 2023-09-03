import os
from flask import Flask, request

app = Flask(__name__)

# Stockage des messages
messages = []

@app.route('/')
def chat():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat GPT</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
            }

            h1 {
                background-color: #333;
                color: #fff;
                text-align: center;
                padding: 10px;
            }

            #chat-container {
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            #chat {
                margin-bottom: 10px;
                padding: 10px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-height: 100px;
                max-height: 300px;
                overflow-y: scroll;
            }

            input[type="text"] {
                width: 80%;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }

            button {
                padding: 5px 10px;
                background-color: #333;
                color: #fff;
                border: none;
                border-radius: 3px;
                cursor: pointer;
            }

            .user-message {
                text-align: right;
                color: #333;
                margin: 5px 0;
            }

            .gpt-message {
                text-align: left;
                color: #0066cc;
                margin: 5px 0;
            }
        </style>
    </head>
    <body>
        <h1>Chat GPT</h1>
        <div id="chat-container">
            <div id="chat"></div>
            <input type="text" id="message" placeholder="Entrez votre message">
            <button id="send">Envoyer</button>
        </div>
        <script>
            var chatDiv = document.getElementById('chat');
            var messageInput = document.getElementById('message');
            var sendButton = document.getElementById('send');

            function addMessage(message, isUser) {
                var messageElement = document.createElement('p');
                messageElement.textContent = (isUser ? 'Vous : ' : 'Gpt : ') + message;
                messageElement.className = isUser ? 'user-message' : 'gpt-message';
                chatDiv.appendChild(messageElement);
            }

            // Gestionnaire d'événement pour le bouton d'envoi
            sendButton.addEventListener('click', function() {
                var message = messageInput.value;
                if (message.trim() !== '') {
                    addMessage(message, true);
                    messageInput.value = '';
                    // Envoyer le message au serveur ou effectuer le traitement souhaité ici
                    // Par exemple, vous pouvez utiliser une requête AJAX pour envoyer le message au serveur Flask
                }
            });
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
