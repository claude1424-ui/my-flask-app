import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def chat():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Flask</title>
    </head>
    <body>
        <h1>Chat Flask</h1>
        <div id="chat-container">
            <div id="chat"></div>
            <input type="text" id="message" placeholder="Entrez votre message">
            <button id="send">Envoyer</button>
        </div>
        <script>
            document.getElementById('send').addEventListener('click', function() {
                var messageInput = document.getElementById('message');
                var message = messageInput.value;
                // Vous pouvez traiter le message ici et envoyer une réponse depuis le serveur Flask
                // Par exemple, en utilisant une requête AJAX pour envoyer le message au serveur
                messageInput.value = ''; // Effacez le champ de texte après avoir envoyé le message
            });
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
