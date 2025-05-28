from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

def get_advice():
    resp = requests.get("https://api.adviceslip.com/advice", timeout=5)
    resp.raise_for_status()
    data = resp.json()
    return data.get('slip', {}).get('advice')

@app.route('/tools/list', methods=['POST'])
def tools_list():
    req = request.get_json()
    return jsonify({
        "jsonrpc": "2.0",
        "id": req.get("id"),
        "result": {
            "tools": [
                {
                    "name": "get_advice",
                    "description": "Get a random advice",
                    "inputSchema": {"type": "object", "properties": {}}
                }
            ]
        }
    })

@app.route('/tools/call', methods=['POST'])
def tools_call():
    req = request.get_json()
    if not req or req.get("params", {}).get("name") != "get_advice":
        return jsonify({"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32601, "message": "Unknown tool"}})
    try:
        advice = get_advice()
        return jsonify({
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "result": {
                "content": [
                    {"type": "text", "text": advice}
                ],
                "isError": False
            }
        })
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "error": {"code": -32000, "message": str(e)}
        })

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Advice MCP is live!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)