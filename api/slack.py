from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    print("Evento recebido:", data)
    return jsonify({"ok": True})

# Vercel usa a variável 'app' como ponto de entrada
handler = app
