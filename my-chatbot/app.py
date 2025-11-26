from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    reply = f"You said: {user_msg}. I'm your embedded bot!"
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Chatbot API is running!"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)
