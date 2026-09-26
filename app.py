from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.environ.get("WHATSAPP_TOKEN")
VERIFY_TOKEN = "barsckel123"

@app.route('/')
def home():
    return "Bot barsckel en ligne!"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Verification failed", 403
    if request.method == 'POST':
        data = request.json
        try:
            entry = data['entry'][0]['changes'][0]['value']
            if 'messages' in entry:
                phone = entry['messages'][0]['from']
                text = entry['messages'][0]['text']['body']
                phone_id = entry['metadata']['phone_number_id']
                reply = f"Salut! Tu as dit: {text}. Bot Barsckel te repond depuis Douala"
                url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
                headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
                payload = {"messaging_product":"whatsapp","to":phone,"text":{"body":reply}}
                requests.post(url, json=payload, headers=headers)
        except: pass
        return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
