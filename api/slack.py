from flask import Flask, request, jsonify
import os, requests, openai

app = Flask(__name__)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Validação do Slack
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # Evento de mensagem
    if "event" in data:
        event = data["event"]
        if event.get("type") == "app_mention":
            text = event.get("text")
            channel = event.get("channel")

            # Resposta com IA
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente de Slack útil e simpático."},
                    {"role": "user", "content": text}
                ]
            )

            reply = completion["choices"][0]["message"]["content"]

            requests.post("https://slack.com/api/chat.postMessage", {
                "token": SLACK_BOT_TOKEN,
                "channel": channel,
                "text": reply
            })

    return "OK", 200

# Exporta o app para o handler da Vercel
app = app
