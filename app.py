import openai
from flask import Flask, request, jsonify

# Configurez votre clé API OpenAI ici
openai.api_key = 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

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data['question']
        
        # Utilisez OpenAI pour obtenir une réponse à la question
        response = openai.Completion.create(
            engine="davinci",  # Choisissez le modèle d'OpenAI approprié
            prompt=f"Répondre à la question suivante : {question}",
            max_tokens=50  # Ajustez le nombre de tokens selon vos besoins
        )
        
        answer = response.choices[0].text.strip()
        
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()
