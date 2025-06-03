#!/usr/bin/env python3
import json
import sys
import requests

def main():
    # Unbuffered I/O
    sys.stdout.reconfigure(line_buffering=True)
    sys.stdin.reconfigure(line_buffering=True)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        try:
            request = json.loads(line)
            method = request.get("method")
            req_id = request.get("id")
            params = request.get("params", {})
            
            # Initialize
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "project-mcp", "version": "1.0.0"}
                    }
                }
            
            # Tools list
            elif method == "tools/list":
                response = {
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
            
            # Tools call
            elif method == "tools/call":
                if params.get("name") != "get_advice":
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": "Unknown tool"}
                    }
                else:
                    try:
                        # Get advice
                        resp = requests.get("https://api.adviceslip.com/advice", timeout=5)
                        resp.raise_for_status()
                        data = resp.json()
                        advice = data.get('slip', {}).get('advice', 'No advice available')
                        
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": advice}]
                            }
                        }
                    except Exception as e:
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "error": {"code": -32000, "message": str(e)}
                        }
            
            # Unknown method
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": "Method not found"}
                }
            
            # Send response
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": "Parse error"},
                "id": None
            }
            print(json.dumps(error_response), flush=True)
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                "id": None
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()