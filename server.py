from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-70b-versatile"    # çok güçlü ve ücretsiz

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    prompt = data.get("prompt", "")

    system_msg = (
        "Sadece TEK SATIRLIK bir bilgisayar kontrol komutu üret. "
        "Formatlar: PRESS w 1 | MOVE_MOUSE 800 450 | CLICK | TYPE Merhaba | OPEN notepad.exe "
        "Açıklama, yorum, açıklayıcı metin YAZMA. Sadece komut döndür."
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    r = requests.post(GROQ_URL, json=payload, headers=headers)
    
    try:
        result = r.json()
        command = result["choices"][0]["message"]["content"].strip()
        return jsonify({"command": command})
    except Exception as e:
        return jsonify({"error": str(e), "raw": r.text}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
