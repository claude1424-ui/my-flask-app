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

            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            h1 {
                background-color: #333;
                color: #fff;
                text-align: center;
                padding: 10px;
            }

            #chat {
                max-height: 400px;
                overflow-y: scroll;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }

            p {
                margin: 5px 0;
            }

            input[type="text"] {
                width: 80%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 3px;
                margin-right: 10px;
            }

            button {
                padding: 10px 15px;
                background-color: #333;
                color: #fff;
                border: none;
                border-radius: 3px;
                cursor: pointer;
            }

            .user-message {
                text-align: right;
                color: #333;
                margin-right: 10px;
                background-color: #d3e0dc;
                border-radius: 5px;
                padding: 5px;
            }

            .gpt-message {
                text-align: left;
                color: #0066cc;
                margin-left: 10px;
                background-color: #e0ecff;
                border-radius: 5px;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chat GPT</h1>
            <div id="chat"></div>
            <div class="input-container">
                <input type="text" id="message" placeholder="Entrez votre message">
                <button id="send">Envoyer</button>
            </div>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            // Le reste de votre code JavaScript ici...
        </script>
    </body>
    </html>
    """
