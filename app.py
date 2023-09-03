import os
import openai
from flask import Flask, request

app = Flask(__name__)

# Configuration de l'API OpenAI (assurez-vous d'ajouter votre propre clé API)
openai.api_key = "YOUR_OPENAI_API_KEY"

# Stockage des messages
messages = []

@app.route('/')
def chat():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat GPT-3</title>
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
        <h1>Chat GPT-3</h1>
        <div id="chat-container">
            <div id="chat"></div>
            <input type="text" id="message" placeholder="Posez une question">
            <button id="send">Envoyer</button>
        </div>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script>
            var chatDiv = document.getElementById('chat');
            var messageInput = document.getElementById('message');
            var sendButton = document.getElementById('send');

            function addMessage(message, isUser) {
                var messageElement = document.createElement('p');
                messageElement.textContent = (isUser ? 'Vous : ' : 'Gpt-3 : ') + message;
                messageElement.className = isUser ? 'user-message' : 'gpt-message';
                chatDiv.appendChild(messageElement);
            }

            // Gestionnaire d'événement pour le bouton d'envoi
            sendButton.addEventListener('click', function() {
                var message = messageInput.value;
                if (message.trim() !== '') {
                    addMessage(message, true);
                    messageInput.value = '';

                    // Envoyer le message au serveur Python pour obtenir une réponse de GPT-3
                    $.ajax({
                        type: 'POST',
                        url: '/ask',
                        data: JSON.stringify({ question: message }),
                        contentType: 'application/json',
                        success: function(data) {
                            addMessage(data.answer, false);
                        }
                    });
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json['question']
    
    # Utilisez OpenAI GPT-3 pour obtenir une réponse à la question
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Répondez à la question suivante : {question}\nRéponse :",
        max_tokens=50
    )

    answer = response.choices[0].text.strip()

    # Ajouter la réponse à la liste des messages
    messages.append(('Vous : ' + question, True))
    messages.append(('Gpt-3 : ' + answer, False))

    return {'answer': answer}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
