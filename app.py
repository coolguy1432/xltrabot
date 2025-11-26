from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows requests from any origin

# Example chatbot logic (replace with real AI later)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    
    if not message:
        return jsonify({"reply": "Please send a message."})
    
    # For now, simple echo response
    reply = f"You said: {message}"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

