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

@app.route('/mcp', methods=['GET', 'POST', 'DELETE'])
def mcp_handler():
    """Handle MCP protocol requests."""
    
    # GET request - Smithery tool discovery
    if request.method == 'GET':
        # Parse configuration from query parameters if any
        config_params = request.args.to_dict()
        
        # Return tools list directly (for Smithery discovery)
        return jsonify({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [{
                    "name": "get_advice",
                    "description": "Get a random advice string",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }]
            }
        })
    
    # DELETE request
    if request.method == 'DELETE':
        return jsonify({"jsonrpc": "2.0", "id": 1, "result": {}})
    
    # POST request - Standard MCP JSON-RPC
    try:
        req = request.get_json()
        if not req:
            return jsonify({
                "jsonrpc": "2.0", 
                "error": {"code": -32600, "message": "Invalid Request"}, 
                "id": None
            })

        method = req.get("method")
        req_id = req.get("id", 1)
        params = req.get("params", {})

        # Initialize method
        if method == "initialize":
            return jsonify({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "project-mcp",
                        "version": "1.0.0"
                    }
                }
            })

        # List tools method
        elif method == "tools/list":
            return jsonify({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [{
                        "name": "get_advice",
                        "description": "Get a random advice string",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }]
                }
            })

        # Call tool method
        elif method == "tools/call":
            tool_name = params.get("name")
            if tool_name != "get_advice":
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32602,
                        "message": f"Unknown tool: {tool_name}"
                    }
                })
            
            advice = get_advice()
            return jsonify({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": advice
                    }]
                }
            })

        # Method not found
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            })

    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": req.get("id", 1) if 'req' in locals() else 1,
            "error": {
                "code": -32603,
                "message": "Internal error"
            }
        })

@app.route('/', methods=['GET'])
def health_check():
    """Return server health status."""
    return jsonify({"status": "MCP server is running", "version": "1.0.0"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)