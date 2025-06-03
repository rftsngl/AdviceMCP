"""Flask MCP server that provides advice functionality."""
import os

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_advice():
    """Fetch a random advice from external API."""
    try:
        resp = requests.get("https://api.adviceslip.com/advice", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        advice = data.get('slip', {}).get('advice')
        if not advice:
            return "No advice available"
        return advice
    except requests.RequestException:
        return "Failed to fetch advice"

# MCP endpoint'ini GET, POST, DELETE destekleyecek şekilde güncelleyelim
@app.route('/mcp', methods=['GET', 'POST', 'DELETE'])
def mcp_handler():
    """Handle MCP protocol requests."""
    
    # GET isteği için tools listesi döndür (Tool Discovery için)
    if request.method == 'GET':
        return jsonify({
            "tools": [{
                "name": "get_advice",
                "description": "Get a random advice string",
                "inputSchema": {"type": "object", "properties": {}}
            }]
        })
    
    # DELETE isteği için boş response
    if request.method == 'DELETE':
        return jsonify({"status": "ok"})
    
    # POST isteği için mevcut MCP protokolü
    req = request.get_json()
    if not req:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None})

    method = req.get("method")
    req_id = req.get("id")
    params = req.get("params", {})

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

    else:
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "Method not found"}
        })

# Smithery için direkt endpoint'ler ekleyelim
@app.route('/tools/list', methods=['GET', 'POST'])
def tools_list():
    """Return list of available tools."""
    return jsonify({
        "tools": [{
            "name": "get_advice",
            "description": "Get a random advice string",
            "inputSchema": {"type": "object", "properties": {}}
        }]
    })

@app.route('/tools/call', methods=['POST'])
def tools_call():
    """Execute tool calls."""
    req = request.get_json() or {}
    if req.get("name") != "get_advice":
        return jsonify({"error": "Unknown tool"}), 400
    
    advice = get_advice()
    return jsonify({
        "content": [{"type": "text", "text": advice}]
    })

@app.route('/', methods=['GET'])
def health_check():
    """Return server health status."""
    return jsonify({"status": "MCP server is running", "version": "1.0.0"})

# Smithery için root endpoint'e MCP handler ekleyelim
@app.route('/', methods=['POST'])
def root_mcp_handler():
    """Handle MCP protocol requests at root."""
    return mcp_handler()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)