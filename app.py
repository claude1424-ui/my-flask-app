import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Emplacement du fichier de données
donnees_fichier = "donnees.txt"

# Charger les données à partir du fichier
def charger_donnees():
    donnees = {}
    if os.path.exists(donnees_fichier):
        with open(donnees_fichier, 'r') as file:
            lines = file.readlines()
            for line in lines:
                question, reponse = line.strip().split(":")
                donnees[question.strip()] = reponse.strip()
    return donnees

# Enregistrer les données dans le fichier
def enregistrer_donnees(donnees):
    with open(donnees_fichier, 'w') as file:
        for question, reponse in donnees.items():
            file.write(f"{question}:{reponse}\n")

# Fonction pour rechercher sur Internet et générer une réponse
def recherche_internet(question):
    # Ici, vous pouvez implémenter votre logique de recherche sur Internet
    # Par exemple, en utilisant des API de moteurs de recherche ou des bibliothèques de web scraping
    # Pour l'exemple, nous retournons simplement un texte fictif
    return f"Réponse générée à partir de la recherche sur Internet pour la question : '{question}'"

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
                messageElement.textContent = (isUser ? 'Vous : ' : 'GPT : ') + message;
                messageElement.className = isUser ? 'user-message' : 'gpt-message';
                chatDiv.appendChild(messageElement);
            }

            // Gestionnaire d'événement pour le bouton d'envoi
            sendButton.addEventListener('click', function() {
                var message = messageInput.value;
                if (message.trim() !== '') {
                    addMessage(message, true);
                    messageInput.value = '';

                    // Envoyer la question au serveur
                    fetch('/process_message', {
                        method: 'POST',
                        body: JSON.stringify({ message: message }),
                        headers: { 'Content-Type': 'application/json' },
                    })
                        .then(response => response.json())
                        .then(data => {
                            addMessage(data.message, false);
                        });
                }
            });
        </script>
    </body>
    </html>
    """

# Route pour traiter les messages
@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    message = data.get('message', '')

    # Charger les données actuelles à partir du fichier
    donnees_apprentissage = charger_donnees()

    # Traitez le message ici et générez la réponse
    if ":" in message:
        question, reponse = message.split(":")
        question = question.strip()
        reponse = reponse.strip()
        donnees_apprentissage[question] = reponse
        enregistrer_donnees(donnees_apprentissage)
        response = f"J'ai appris la réponse à la question : '{question}'"
    else:
        if message in donnees_apprentissage:
            reponse = donnees_apprentissage[message]
            response = "GPT : " + reponse
        else:
            # Si la question n'est pas trouvée dans les données, effectuer une recherche sur Internet
            reponse = recherche_internet(message)
            response = "GPT : " + reponse

    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
