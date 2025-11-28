from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-70b-versatile"

MEMORY_FILE = "memory.txt"

def save_memory(prompt, command, status):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"PROMPT: {prompt}\nCOMMAND: {command}\nSTATUS: {status}\n---\n")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return ""
    return open(MEMORY_FILE, "r", encoding="utf-8").read()

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    prompt = data.get("prompt", "")
    status = data.get("status", "unknown")

    memory_text = load_memory()

    system_msg = (
        "Sen bilgisayar kontrol ajanısın. "
        "Görev: TEK SATIR komut üret. Açıklama yok.\n"
        "Format: PRESS w 1 | MOVE_MOUSE 800 450 | CLICK | TYPE yazı | OPEN app.exe\n"
        "Geçmiş hafıza:\n" + memory_text
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(GROQ_URL, json=payload, headers=headers)
    result = r.json()
    command = result["choices"][0]["message"]["content"].strip()

    save_memory(prompt, command, status)

    return jsonify({"command": command})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
