from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# API anahtarını ortam değişkeninden alacağız
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    prompt = data.get("prompt", "")

    # Burada hep KOMUT formatı üretmesini isteyebilirsin
    system_msg = (
        "Bilgisayarı kontrol etmek için sadece komut üret. "
        "Format örnekleri: "
        "PRESS w 2 | MOVE_MOUSE 800 400 | CLICK | TYPE Merhaba | OPEN notepad.exe. "
        "Açıklama yazma, sadece tek satır komut döndür."
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    )

    output = completion.choices[0].message.content.strip()
    return jsonify({"command": output})

if __name__ == "__main__":
    # Render kendi portunu verecek, ama lokalde test için 5000:
    app.run(host="0.0.0.0", port=5000)
