from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

def get_advice():
    try:
        resp = requests.get("https://api.adviceslip.com/advice", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        advice = data.get('slip', {}).get('advice')
        if not advice:
            return "No advice available"
        return advice
    except Exception:
        return "Failed to fetch advice"

@app.route('/mcp', methods=['POST'])
def mcp_handler():
    req = request.get_json()
    if not req:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None})

    method = req.get("method")
    req_id = req.get("id")
    params = req.get("params", {})

    # Initialize
    if method == "initialize":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "project-mcp", "version": "1.0.0"}
            }
        })

    # Tools list
    elif method == "tools/list":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [{
                    "name": "get_advice",
                    "description": "Get a random advice string",
                    "inputSchema": {"type": "object", "properties": {}}
                }]
            }
        })

    # Tools call
    elif method == "tools/call":
        if params.get("name") != "get_advice":
            return jsonify({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": "Unknown tool"}
            })
        
        advice = get_advice()
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": advice}]
            }
        })

    # Unknown method
    else:
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "Method not found"}
        })

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "MCP server is running", "version": "1.0.0"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)