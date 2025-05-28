from flask import Flask, jsonify
import requests

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

if __name__ == '__main__':
    app.run(port=5000)
