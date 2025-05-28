from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
ADVICE_URL = "https://api.adviceslip.com/advice"

@app.route('/mcp/advice', methods=['GET'])
def get_advice():
    try:
        resp = requests.get(ADVICE_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return jsonify({
            'advice': data.get('slip', {}).get('advice')
        })
    except Exception as e:
        print("API çağrısı hatası:", e)
        return jsonify({'error': 'Servis çağrısında hata oluştu.'}), 502

@app.route('/', methods=['GET'])
def home():
    return "MCP API çalışıyor!"

if __name__ == '__main__':
    # Portu buluttan al, yoksa 5000 kullan
    port = int(os.environ.get("PORT", 5000))
    # Her yerden erişim için host=0.0.0.0
    app.run(host="0.0.0.0", port=port)
