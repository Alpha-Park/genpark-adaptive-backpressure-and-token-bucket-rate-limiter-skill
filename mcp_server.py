"""MCP server for Adaptive Backpressure Rate Limiter."""
import sys
import json
from client import AdaptiveBackpressureRateLimiter

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "evaluate_request",
                    "description": "Assess rate limit and concurrency backpressure for incoming agent tool requests",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "client_id": {"type": "string"},
                            "tokens_available": {"type": "number"},
                            "token_cost": {"type": "number", "default": 1.0},
                            "concurrency_active": {"type": "integer", "default": 0},
                            "concurrency_limit": {"type": "integer", "default": 15},
                            "refill_rate_per_sec": {"type": "number", "default": 5.0}
                        },
                        "required": ["client_id", "tokens_available"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "evaluate_request":
            out = AdaptiveBackpressureRateLimiter.evaluate_request(
                args.get("client_id", "unknown"),
                float(args.get("tokens_available", 0.0)),
                float(args.get("token_cost", 1.0)),
                int(args.get("concurrency_active", 0)),
                int(args.get("concurrency_limit", 15)),
                float(args.get("refill_rate_per_sec", 5.0))
            )
            return {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
    return {"error": "Unsupported method or tool"}

if __name__ == "__main__":
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
