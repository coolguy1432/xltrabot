from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- add this

app = Flask(__name__)
CORS(app)  # <-- enable cross-origin requests

@app.route("/")
def home():
    return "Chatbot API is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({"reply": f"You said: {message}. I'm your embedded bot!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
