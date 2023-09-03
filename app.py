from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionnaire pour stocker les données d'apprentissage
donnees_apprentissage = {}

# Charger les données depuis un fichier JSON (si nécessaire)
def charger_donnees():
    try:
        with open('donnees.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Enregistrer les données dans un fichier JSON
def enregistrer_donnees():
    with open('donnees.json', 'w') as file:
        json.dump(donnees_apprentissage, file)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat GPT</title>
    </head>
    <body>
        <h1>Chat GPT</h1>
        <div id="chat"></div>
        <input type="text" id="message" placeholder="Posez une question">
        <button id="send">Envoyer</button>
        
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script>
            $(document).ready(function() {
                var chatDiv = $("#chat");
                var messageInput = $("#message");
                var sendButton = $("#send");

                // Fonction pour afficher un message dans le chat
                function showMessage(message, sender) {
                    var messageClass = sender === "Vous" ? "user-message" : "gpt-message";
                    chatDiv.append("<p class='" + messageClass + "'>" + message + "</p>");
                }

                // Fonction pour envoyer un message
                function sendMessage() {
                    var utilisateur_question = messageInput.val();
                    showMessage("Vous : " + utilisateur_question, "Vous");

                    if (utilisateur_question.toLowerCase() === "au revoir") {
                        showMessage("GPT : Au revoir! À la prochaine.", "GPT");
                        // Enregistrez les données dans un fichier ici si nécessaire
                    } else if (utilisateur_question.includes(":")) {
                        var [question, reponse] = utilisateur_question.split(":");
                        question = question.trim();
                        reponse = reponse.trim();
                        donnees_apprentissage[question] = reponse;
                        enregistrer_donnees();
                        showMessage("GPT : J'ai appris la réponse à la question : " + question, "GPT");
                    } else {
                        var reponse = donnees_apprentissage[utilisateur_question] || "Je ne connais pas la réponse à cette question.";
                        showMessage("GPT : " + reponse, "GPT");
                    }

                    messageInput.val("");  // Effacez l'entrée utilisateur
                }

                // Gestionnaire de clic sur le bouton "Envoyer"
                sendButton.click(sendMessage);

                // Gestionnaire de pression de touche pour la touche "Entrée"
                messageInput.keypress(function(event) {
                    if (event.keyCode === 13) {
                        sendMessage();
                    }
                });
            });
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    donnees_apprentissage = charger_donnees()  # Chargez les données depuis le fichier JSON (si disponible)
    app.run(debug=True)
