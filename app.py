import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai

load_dotenv()
app = Flask(__name__)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # ✅ Validação inicial do Slack (challenge)
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event = data["event"]

        # Verifica se é uma menção ao bot
        if event.get("type") == "app_mention":
            user = event.get("user")
            text = event.get("text")
            channel = event.get("channel")

            # 🔮 Gera resposta com IA
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente de Slack amigável e útil."},
                    {"role": "user", "content": text}
                ]
            )

            reply = response["choices"][0]["message"]["content"]

            # 💬 Envia resposta ao Slack
            requests.post("https://slack.com/api/chat.postMessage", {
                "token": SLACK_BOT_TOKEN,
                "channel": channel,
                "text": reply
            })

    return "OK", 200

if __name__ == "__main__":
    app.run(port=3000)
