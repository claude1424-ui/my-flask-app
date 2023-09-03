from flask import Flask
from flask_socketio import SocketIO
from datetime import datetime
import webbrowser
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Define CSS styles directly in the program
css_style = """
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

    #chat {
        max-width: 600px;
        margin: 0 auto;
        padding: 10px;
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    p {
        margin: 5px 0;
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
        margin-left: 10px;
        color: #333;
    }

    .gpt-message {
        text-align: left;
        margin-right: 10px;
        color: #0066cc;
    }
</style>
"""

# List to store chat messages
message_history = []

@app.route('/')
def chat():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat GPT</title>
        """ + css_style + """
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>Chat GPT</h1>
        <div id="chat"></div>
        <input type="text" id="message" placeholder="Entrez votre message">
        <button id="send">Envoyer</button>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            var socket = io.connect('http://' + document.domain + ':' + location.port);

            // Function to display a message in the chat
            function showMessage(message, isUser) {
                var chatDiv = document.getElementById('chat');
                var newMessage = document.createElement('p');
                newMessage.innerHTML = message; // Use innerHTML to display HTML content

                // Reverse CSS classes based on the message sender
                if (isUser) {
                    newMessage.className = 'user-message';  // User on the left
                } else {
                    newMessage.className = 'gpt-message';  // GPT on the right
                }

                chatDiv.appendChild(newMessage);
            }

            // Display message history when the page loads
            socket.on('message_history', function(history) {
                for (var i = 0; i < history.length; i++) {
                    showMessage(history[i][0], history[i][1]);
                }
            });

            socket.on('message', function(message) {
                showMessage(message, false);
            });

            document.getElementById('send').addEventListener('click', function() {
                var messageInput = document.getElementById('message');
                var message = messageInput.value;
                socket.emit('message', message);
                // Add your name or 'GPT' to the message
                showMessage('Vous : ' + message, true);  // For your messages
                messageInput.value = '';
            });
        </script>
    </body>
    </html>
    """

def search_google(query):
    try:
        search_results = search(query, num_results=3)
        return list(search_results)
    except Exception:
        return []

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        return text.strip()
    except Exception:
        return None

def generate_summary(text_content):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text_content)

    # Remove stopwords and non-alphanumeric words
    stop_words = set(stopwords.words("english"))
    filtered_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        filtered_sentence = [word for word in words if word not in stop_words and word.isalnum()]
        filtered_sentences.append(" ".join(filtered_sentence))

    # Combine the filtered sentences into a summary
    summary = " ".join(filtered_sentences)

    # Trim the summary to be between 10 and 500 characters
    if len(summary) < 10:
        return summary
    elif len(summary) > 500:
        return summary[:500]
    else:
        return summary

@socketio.on('message')
def handle_message(message):
    message = message.lower()
    
    if 'quelle' in message and 'heure' in message:
        current_time = datetime.now().strftime("%H:%M")
        response = f'GPT : Il est actuellement {current_time}.'
    elif message == 'bonjour':
        response = 'GPT : Bonjour'
    else:
        # Search on Google
        search_results = search_google(message)

        if not search_results:
            response = "GPT : Je n'ai trouvé aucun résultat sur Internet."
        else:
            # Extract text from the first search result URL
            first_result_url = search_results[0]
            text_content = extract_text_from_url(first_result_url)

            if not text_content:
                response = "GPT : Je n'ai pas pu extraire le contenu de la page Web."
            else:
                # Generate a summary of the extracted text
                summary = generate_summary(text_content)
                response = f'GPT : {summary}'

    message_history.append(('Vous : ' + message, True))
    message_history.append((response, False))
    socketio.send(response)
    socketio.emit('message_history', message_history, broadcast=False)

if __name__ == '__main__':
    webbrowser.open_new('http://0.0.0.0:8080/')
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
