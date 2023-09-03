import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

donnees_fichier = "donnees.txt"
donnees_url = "https://raw.githubusercontent.com/claude1424-ui/my-flask-app/main/donnees.txt"

def charger_donnees():
    donnees = {}
    if os.path.exists(donnees_fichier):
        with open(donnees_fichier, 'r') as file:
            lines = file.readlines()
            for line in lines:
                question, reponse = line.strip().split(":")
                donnees[question.strip()] = reponse.strip()
    else:
        try:
            response = requests.get(donnees_url)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for line in lines:
                    question, reponse = line.strip().split(":")
                    donnees[question.strip()] = reponse.strip()
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
    return donnees

def enregistrer_donnees(donnees):
    with open(donnees_fichier, 'w') as file:
        for question, reponse in donnees.items():
            file.write(f"{question}:{reponse}\n")
    data_to_save = "\n".join([f"{question}:{reponse}" for question, reponse in donnees.items()])
    try:
        response = requests.put(donnees_url, data=data_to_save)
        if response.status_code == 200:
            print("Données enregistrées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des données : {e}")

def recherche_internet(question):
    # Implémentez ici votre logique de recherche sur Internet
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

            sendButton.addEventListener('click', function() {
                var message = messageInput.value;
                if (message.trim() !== '') {
                    addMessage(message, true);
                    messageInput.value = '';

                    fetch('/process_message', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message: message }),
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

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    message = data.get('message', '')

    donnees_apprentissage = charger_donnees()

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
            reponse = recherche_internet(message)
            response = "GPT : " + reponse

    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
