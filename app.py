from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("HF_API_KEY environment variable not set!")

# You can pick any model available on Hugging Face Inference API
# Some free ones: 'facebook/opt-1.3b', 'tiiuae/falcon-7b-instruct', 'mpt-7b-chat'
HF_MODEL = "facebook/opt-1.3b"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    payload = {
        "inputs": user_message
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        response_json = response.json()
        if "error" in response_json:
            return jsonify({"error": response_json["error"]}), 500
        # Hugging Face returns output in different formats depending on model
        if isinstance(response_json, list):
            reply = response_json[0].get("generated_text", "Sorry, I couldn't respond.")
        elif isinstance(response_json, dict) and "generated_text" in response_json:
            reply = response_json["generated_text"]
        else:
            reply = str(response_json)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
