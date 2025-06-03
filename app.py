import json
import sys
import logging

# Logging'i stderr'e yönlendir (stdio ile karışmaması için)
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
logger = logging.getLogger(__name__)

def get_advice():
    import requests
    try:
        resp = requests.get("https://api.adviceslip.com/advice", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        advice = data.get('slip', {}).get('advice')
        if not advice:
            raise ValueError("No advice received from API")
        return advice
    except Exception as e:
        logger.error(f"Failed to get advice: {e}")
        raise RuntimeError(f"Failed to fetch advice: {e}")

def handle_request(request):
    logger.debug(f"Handling request: {request}")
    
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})
    
    if method == "initialize":
        response = {
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
        }
        logger.debug(f"Initialize response: {response}")
        return response
    
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
        logger.debug(f"Tools list response: {response}")
        return response
    
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
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32000, "message": str(e)}
            }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "Method not found"}
        }

def main():
    logger.info("MCP server starting...")
    
    # sys.stdin'i line buffered yap
    sys.stdin.reconfigure(line_buffering=True)
    sys.stdout.reconfigure(line_buffering=True)
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            logger.debug(f"Received line: {line}")
            
            try:
                request = json.loads(line)
                response = handle_request(request)
                response_json = json.dumps(response)
                print(response_json, flush=True)
                logger.debug(f"Sent response: {response_json}")
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": "Parse error"},
                    "id": None
                }
                print(json.dumps(error_response), flush=True)
                
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == '__main__':
    main()