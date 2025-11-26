from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import time

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("HF_API_KEY environment variable not set!")

# Pick a free, smaller model for fast responses
HF_MODEL = "tiiuae/falcon-7b-instruct"  # works well for chat

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
        "inputs": user_message,
        "parameters": {"max_new_tokens": 200}
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        res_json = response.json()

        # Some models return {'error': 'message'} if not ready
        if "error" in res_json:
            return jsonify({"error": res_json["error"]}), 500

        # Try to extract generated_text
        if isinstance(res_json, dict) and "generated_text" in res_json:
            reply = res_json["generated_text"]
        elif isinstance(res_json, list) and "generated_text" in res_json[0]:
            reply = res_json[0]["generated_text"]
        else:
            reply = str(res_json)

        # Trim the user's message from the response if model echoes
        if reply.lower().startswith(user_message.lower()):
            reply = reply[len(user_message):].strip()

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

