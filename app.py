import json
import sys
import requests

def get_advice():
    resp = requests.get("https://api.adviceslip.com/advice", timeout=5)
    resp.raise_for_status()
    data = resp.json()
    return data.get('slip', {}).get('advice')

def handle_request(request):
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "serverInfo": {
                    "name": "project-mcp",
                    "version": "1.0.0"
                }
            }
        }
    
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [{
                    "name": "get_advice",
                    "description": "Get a random advice string",
                    "inputSchema": {"type": "object", "properties": {}}
                }]
            }
        }
    
    elif method == "tools/call":
        if params.get("name") != "get_advice":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": "Unknown tool"}
            }
        try:
            advice = get_advice()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": advice}]
                }
            }
        except Exception:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32000, "message": "An error occurred"}
            }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "Method not found"}
        }

def main():
    for line in sys.stdin:
        if line.strip():
            try:
                request = json.loads(line)
                response = handle_request(request)
                print(json.dumps(response), flush=True)
            except Exception:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": "Parse error"}
                }
                print(json.dumps(error_response), flush=True)

if __name__ == '__main__':
    main()