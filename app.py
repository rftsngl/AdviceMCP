from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_advice():
    resp = requests.get("https://api.adviceslip.com/advice", timeout=5)
    resp.raise_for_status()
    data = resp.json()
    return data.get('slip', {}).get('advice')

# MCP endpoint: /tools/list
@app.route('/tools/list', methods=['POST'])
def tools_list():
    return jsonify({
        "result": [
            {
                "name": "get_advice",
                "description": "Get a random advice string",
                "parameters": {},
                "returns": {
                    "type": "string",
                    "description": "Random advice"
                }
            }
        ]
    })

# MCP endpoint: /tools/call
@app.route('/tools/call', methods=['POST'])
def tools_call():
    req = request.get_json()
    if not req or req.get("name") != "get_advice":
        return jsonify({"error": "Unknown tool or missing name"}), 400
    try:
        advice = get_advice()
        return jsonify({"result": advice})
    except Exception as e:
        return jsonify({"error": str(e)}), 502

# MCP zorunlu kök endpoint (bazı durumlarda isteniyor)
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "MCP-compatible Advice API"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
