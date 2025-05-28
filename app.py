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

@app.route('/mcp', methods=['POST'])
def mcp_entrypoint():
    req = request.get_json()
    print("GELEN MCP İSTEĞİ:", req, flush=True)
    if not req or "method" not in req:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None})

    method = req["method"]
    req_id = req.get("id")
    params = req.get("params", {})

    if method == "initialize":
        # MCP initialize methoduna basit bir cevap dön
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {"message": "initialized"}})

    elif method == "tools.list":
        result = [
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
        return jsonify({"jsonrpc": "2.0", "result": result, "id": req_id})

    elif method == "tools.call":
        if params.get("name") != "get_advice":
            return jsonify({"jsonrpc": "2.0", "error": {"code": -32601, "message": "Unknown tool"}, "id": req_id})
        try:
            advice = get_advice()
            return jsonify({"jsonrpc": "2.0", "result": advice, "id": req_id})
        except Exception as e:
            return jsonify({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}, "id": req_id})

    else:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id})

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Advice MCP is live!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)