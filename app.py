import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message'].lower()
    
    # Ajoutez ici votre logique de chat GPT en réponse au message de l'utilisateur.
    # Vous pouvez utiliser les bibliothèques nécessaires pour votre logique de chat.

    # Exemple de réponse :
    response = {"message": "Ceci est la réponse de GPT."}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

